from struct import unpack
import cv2
from numpy import mod, power
import sympy
from chunk_reader import append_hex
from keys_generator import KeysGenerator
import sympy
from gmpy2 import mpz
from PIL import Image 
from Crypto.Cipher import AES 
import rsa

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'

class Encrypter():
    def __init__(self, file):
        self.filename = file
        self.f = open(file, 'rb')
        if self.f.read(len(PNG_SIGNATURE)) != PNG_SIGNATURE:
            raise Exception('Invalid PNG Signature')

    def encrypt(self):
        #self.encryptFromLibrary()
        path = self.filename.split('/')
        clearFilename = path[len(path) - 1]
        encryptedPixelsName = "encrypted_pixels_" + clearFilename[:-4] + ".dat"
        keysGenerator = KeysGenerator()
        keysGenerator.generateNewKeys()
        (pubKey, privKey) = keysGenerator.getKeysFromFile()
        image = cv2.imread(self.filename)
        rows, cols, _ = image.shape
        f = open("encrypted_test_images/" + encryptedPixelsName, "w")
        data = [ [ [ 0 for i in range(image.shape[2]) ] for j in range(image.shape[1]) ] for k in range(image.shape[0])]
        for i in range(rows):
            for j in range(cols):
                for k in range(3):
                    data[i][j][k] = image[i,j,k]
                    data[i][j][k] = pow(mpz(data[i][j][k]), pubKey[0], pubKey[1])
                    image[i,j,k] = sympy.Mod(data[i][j][k] ,256)
                    f.write(str(data[i][j][k]) + ", ")
                f.write("\n")
        encryptedImgName = "encrypted_" + path[len(path) - 1]
        cv2.imwrite("encrypted_test_images/" + encryptedImgName, image)
        self.encryptECB(self.filename, b"1234567890abcdef")
        f.close()

    def pad(self,data):
        return data + b"\x00"*(16-len(data)%16)
    
    def toRGB(self, data):
        r, g, b = tuple(map(lambda d: [data[i] for i in range(0,len(data)) if i % 3 == d], [0, 1, 2])) 
        pixels = tuple(zip(r,g,b)) 
        return pixels

    def aes_ecb_encrypt(self, key, data, mode=AES.MODE_ECB): 
        aes = AES.new(key, mode) 
        outData = aes.encrypt(data) 
        return outData

    def encryptECB(self, filename, key):
        path = filename.split('/')
        clearFilename = path[len(path) - 1]
        im = Image.open(filename) 
        data = im.convert("RGB").tobytes()
        originalData = len(data) 
        encodedData = self.toRGB(self.ecb_encrypt(key, self.pad(data))[:originalData])
        im2 = Image.new(im.mode, im.size) 
        im2.putdata(encodedData)
        outFilename = "ecb_" + clearFilename
        im2.save("encrypted_test_images/" + outFilename, "PNG")

    def ecb_encrypt(self, key, data, mode=AES.MODE_ECB): 
        aes = AES.new(key, mode) 
        encryptedData = aes.encrypt(data) 
        return encryptedData

    def encryptFromLibrary(self):
        (pubKey, privKey) = rsa.newkeys(1024)
        with open("keys/RSA_public_key.pem", "wb") as f:
            f.write(pubKey.save_pkcs1("PEM"))
        
        with open("keys/RSA_private_key.pem", "wb") as f:
            f.write(privKey.save_pkcs1("PEM"))

        path = self.filename.split('/')
        clearFilename = path[len(path) - 1]
        encryptedPixelsName = "RSA_encrypted_pixels_" + clearFilename[:-4] + ".dat"

        image = cv2.imread(self.filename)
        rows, cols, _ = image.shape
        f = open("encrypted_test_images/" + encryptedPixelsName, "w")
        data = [ [ [ 0 for i in range(image.shape[2]) ] for j in range(image.shape[1]) ] for k in range(image.shape[0])]
        for i in range(rows):
            for j in range(cols):
                for k in range(3):
                    data[i][j][k] = int(image[i,j,k])
                    data[i][j][k] = rsa.encrypt(data[i][j][k].to_bytes(2,'big'), pubKey)
                    image[i,j,k] = sympy.Mod(int.from_bytes(data[i][j][k],'big') ,256)
                    f.write(str(int.from_bytes(data[i][j][k], "big")) + ", ")
                f.write("\n")
        encryptedImgName = "RSA_encrypted_" + path[len(path) - 1]
        cv2.imwrite("encrypted_test_images/" + encryptedImgName, image)
        f.close()
