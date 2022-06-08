from struct import unpack
import struct
from sys import byteorder
from numpy import  mod, power
import numpy
import cv2
from gmpy2 import mpz

from keys_generator import KeysGenerator


class Decrypter:
  def __init__(self, filename):
    self.filename = filename

  def decrypt(self):
    path = self.filename.split('/')
    clearFilename = path[len(path) - 1]
    encryptedImage = "encrypted_test_images/encrypted_" + clearFilename
    image = cv2.imread(encryptedImage)
    rows, cols, colors = image.shape
    encryptedData = [ [ [ 0 for i in range(image.shape[2]) ] for j in range(image.shape[1]) ] for k in range(image.shape[0])]
    encryptedPixels = "encrypted_test_images/encrypted_pixels_" + clearFilename[:-4] + ".dat"
    with open(encryptedPixels) as f:
      for i in range(rows):
        for j in range(cols):
            line = f.readline()
            data = line.split(", ")
            encryptedData[i][j] = data

    generator = KeysGenerator()
    (pubKey, privKey) = generator.getKeysFromFile()
    for i in range(rows):
      for j in range(cols):
        for k in range(colors):
          image[i,j,k] = pow(int(encryptedData[i][j][k]), privKey[0], privKey[1])
    cv2.imwrite("decrypted_test_images/decrypted_" + clearFilename, image)
