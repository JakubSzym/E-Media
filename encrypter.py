
from struct import unpack
import struct
from numpy import mod, power

from keys_generator import KeysGenerator

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'

class Encrypter():
    def __init__(self, file):
        self.filename = file
        self.image_data = []
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
        (pubKey, privKey) = keysGenerator.getKeysFromFile()
       

        for type, length, data, crc in self.image_data:
            if type == b'IDAT':
                length *= 4
                bites = length.to_bytes(4, byteorder = 'big')
                f.write(bites)
                f.write(type)
                for byte in data:
                    encryptedValue = int(mod(byte ** pubKey[0], pubKey[1]))
                    encryptedByte = encryptedValue.to_bytes(4, byteorder = 'big')
                    f.write(encryptedByte)
            else:
                bites = length.to_bytes(4, byteorder = 'big')
                f.write(bites)
                f.write(type)
                f.write(data)
            f.write(crc[0])
        f.close()