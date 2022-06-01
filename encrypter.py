from struct import unpack
import struct
import cv2
from numpy import mod, power
import sympy
from chunk_reader import append_hex
from keys_generator import KeysGenerator
import keys_generator
import numpy
import sympy
import gmpy2

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
        image = cv2.imread(self.filename)
        rows, cols, _ = image.shape
        #data = numpy.zeros(image.shape)
        data = [ [ [ 0 for i in range(image.shape[2]) ] for j in range(image.shape[1]) ] for k in range(image.shape[0])]
        
        for i in range(rows):
            for j in range(cols):
                for k in range(3):
                    data[i][j][k] = image[i,j,k]
                    data[i][j][k] = pow(int(data[i][j][k]), pubKey[0], pubKey[1])
                    image[i,j,k] = sympy.Mod(data[i][j][k] ,256)
        cv2.imwrite("test_images/lin.png", image)