from struct import unpack
import struct
from sys import byteorder
from numpy import  mod, power
import numpy
import cv2
from gmpy2 import mpz

from keys_generator import KeysGenerator


class Decrypter:
  def __init__(self, encryptedData, outImage, filename) -> None:
    self.inData = encryptedData
    self.outImage = outImage
    self.filename = filename
  
  def decrypt(self):
    generator = KeysGenerator()
    generator.getKeysFromFile()
    rows, cols, colors = self.outImage.shape
    for i in range(rows):
      for j in range(cols):
        for k in range(colors):
          self.inData[i][j][k] = generator.decrypt(mpz(self.inData[i][j][k]))
          self.outImage[i,j,k] = self.inData[i][j][k]
    cv2.imwrite("test_images/decoded.png", self.outImage)
