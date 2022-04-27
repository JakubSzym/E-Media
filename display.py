from sys import flags
import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

def display(file):
  img = cv2.imread(file,0)
  
  img_float32 = np.float32(img)

  dft = cv2.dft(img_float32, flags = cv2.DFT_COMPLEX_OUTPUT)
  dft_shift = np.fft.fftshift(dft)

  magnitudeSpectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
  phaseSpectrum = np.log(cv2.phase(dft_shift[:,:,0],dft_shift[:,:,1]))

  img = mpimg.imread(file)

  plt.figure(1)

  plt.subplot(131),plt.imshow(img)
  plt.title('Input image')
  plt.xticks([])
  plt.yticks([])

  plt.subplot(132)
  plt.imshow(magnitudeSpectrum, cmap='gray')
  plt.title('Magnitude spectrum')
  plt.xticks([])
  plt.yticks([])
  
  plt.subplot(133)
  plt.imshow(phaseSpectrum, cmap='gray')
  plt.title('Phase spectrum')
  plt.xticks([])
  plt.yticks([])
  plt.show()

def checkFFT():
  imgStraight = cv2.imread("test_images/Lorem-Ipsum.png", 0)
  imgSkew  = cv2.imread("test_images/Lorem-Ipsum-krzywe.png", 0)

  imgStraight_float32 = np.float32(imgStraight)
  imgSkew_float32 = np.float32(imgSkew)

  dftStraight = cv2.dft(imgStraight_float32 ,flags=cv2.DFT_COMPLEX_OUTPUT)
  dftStraight_shift = np.fft.fftshift(dftStraight)

  dftSkew = cv2.dft(imgSkew_float32, flags=cv2.DFT_COMPLEX_OUTPUT)
  dftSkew_shift = np.fft.fftshift(dftSkew)

  magnitudeSpectrumStraight = 20*np.log(cv2.magnitude(dftStraight_shift[:,:,0], dftStraight_shift[:,:,1]))
  magnitudeSpectrumSkew = 20*np.log(cv2.magnitude(dftSkew_shift[:,:,0], dftSkew_shift[:,:,1]))

  imgStraight = mpimg.imread("test_images/Lorem-Ipsum.png")
  imgSkew = mpimg.imread("test_images/Lorem-Ipsum-krzywe.png")

  plt.figure(2)

  plt.subplot(221)
  plt.imshow(imgStraight)
  plt.title("Straight image")
  plt.xticks([])
  plt.yticks([])

  plt.subplot(222)
  plt.imshow(magnitudeSpectrumStraight, cmap="gray")
  plt.title("Straight image spectrum")
  plt.xticks([])
  plt.yticks([])

  plt.subplot(223)
  plt.imshow(imgSkew)
  plt.title("Skew image")
  plt.xticks([])
  plt.yticks([])

  plt.subplot(224)
  plt.imshow(magnitudeSpectrumSkew, cmap="gray")
  plt.title("Skew image spectrum")
  plt.xticks([])
  plt.yticks([])

  plt.show()

