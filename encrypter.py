from struct import unpack
import struct
from numpy import mod, power
from chunk_reader import append_hex
from keys_generator import KeysGenerator
import keys_generator

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'

class Encrypter():
    def __init__(self, file):
        self.filename = file
        self.image_data = []
        self.block_size = keys_generator.M / 4 - 1
        self.f = open(file, 'rb')
        if self.f.read(len(PNG_SIGNATURE)) != PNG_SIGNATURE:
            raise Exception('Invalid PNG Signature')

    def encrypt(self):
        while(True):
            chunk_length,  = unpack('>I', self.f.read(4))
            chunk_type, = unpack('4s', self.f.read(4))
            chunk_data = self.f.read(chunk_length)
            chunk_crc = unpack('4s', self.f.read(4)) 
            self.image_data.append((chunk_type, chunk_length, chunk_data, chunk_crc))
            if(chunk_type == b'IEND'):
                break
            
        path = self.filename.split('/')
        encryptedImgName = "encrypted_" + path[len(path) - 1]
        f = open(encryptedImgName,"wb")
        f.write(PNG_SIGNATURE)
        keysGenerator = KeysGenerator()
        keysGenerator.generateNewKeys()
        (pubKey, privKey) = keysGenerator.getKeysFromFile()
       
        for type, length, data, crc in self.image_data:
            if type == b'IDAT':
                rest = length % self.block_size
                blocks = length / self.block_size
                rest = int(rest)
                blocks = int(blocks)
                byte_sum = 0x00
                num_bytes = 0
                bites = int(length + blocks + self.block_size - rest + 1).to_bytes(4, byteorder = 'big')
                f.write(bites)
                f.write(type)
                for byte in data:
                    if blocks != 0:
                        byte_sum  = append_hex(byte_sum, byte)
                        num_bytes += 1
                        if num_bytes == self.block_size:
                            encrypted_value = pow(byte_sum, pubKey[0], pubKey[1])
                            encrypted_byte = encrypted_value.to_bytes(int(self.block_size + 1), byteorder = 'big')
                            f.write(encrypted_byte)
                            num_bytes = 0
                            byte_sum = 0
                            blocks -= 1
                    elif rest != 0:
                        byte_sum  = append_hex(byte_sum, byte)
                        num_bytes += 1
                        if num_bytes == rest:
                            encrypted_value = pow(byte_sum, pubKey[0], pubKey[1])
                            encrypted_byte = encrypted_value.to_bytes(int(self.block_size + 1), byteorder = 'big')
                            f.write(encrypted_byte)
            else:
                bites = length.to_bytes(4, byteorder = 'big')
                f.write(bites)
                f.write(type)
                f.write(data)
            f.write(crc[0])
        f.close()