from struct import unpack
import cv2
from numpy import mod, power
import sympy
from chunk_reader import append_hex
from keys_generator import KeysGenerator
import sympy
from gmpy2 import mpz
import rsa

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'

class Encrypter():
    def __init__(self, file):
        self.filename = file
        self.f = open(file, 'rb')
        if self.f.read(len(PNG_SIGNATURE)) != PNG_SIGNATURE:
            raise Exception('Invalid PNG Signature')

    def encrypt(self):
        self.encryptFromLibrary()
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
        f.close()

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
