#!/usr/bin/env python3

# RSA encoding and decoding

import cv2
import numpy
from gmpy2 import mpz

keyOne = 101
keyTwo = 103
exponent = 7

def encode(item, keyOne, keyTwo, exponent):
  n = keyTwo * keyOne
  encoded = pow(mpz(item), exponent) % n
  return encoded

def decode(item, keyOne, keyTwo, exponent):
  n = keyTwo * keyOne
  phi = (keyTwo - 1 ) * (keyOne -1)
  decryptionKey = pow(exponent, -1, phi)
  decoded = pow(mpz(item), mpz(decryptionKey), n)
  return decoded

def encodeImage(image):
  rows, cols, _ = image.shape
  data = numpy.zeros(image.shape)

  for i in range(rows):
    for j in range(cols):
      for k in range(3):
        data[i,j,k] = image[i,j,k]
        data[i][j][k] = encode(data[i][j][k], keyOne, keyTwo, exponent)
        image[i,j,k] = data[i,j,k] % 256
        print(image[i,j,k])

  cv2.imwrite("test_images/lin.png", image)
  return data, image

def decodeImage(data, img):
  rows, cols, _ = data.shape
  for i in range(rows):
    for j in range(cols):
      for k in range(3):
        data[i][j][k] = decode(data[i][j][k], keyOne, keyTwo, exponent)
        img[i,j,k] = numpy.uint8(data[i,j,k])

  cv2.imwrite("ostatnia_decoded.png", img)
  return data

