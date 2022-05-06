import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

def display(file):
  img = cv2.imread(file,0)
  
  ft = np.fft.fft2(img)
  ft_shift = np.fft.fftshift(ft)

  magnitudeSpectrum = 20*np.log(np.abs(ft_shift))
  phaseSpectrum = np.angle(ft_shift)

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

  dftStraight = np.fft.fft2(imgStraight)
  dftStraight_shift = np.fft.fftshift(dftStraight)

  dftSkew = np.fft.fft2(imgSkew)
  dftSkew_shift = np.fft.fftshift(dftSkew)

  magnitudeSpectrumStraight = 20*np.log(np.abs(dftStraight_shift))
  magnitudeSpectrumSkew = 20*np.log(np.abs(dftSkew_shift))

  imgStraight = mpimg.imread("test_images/Lorem-Ipsum.png")
  imgSkew = mpimg.imread("test_images/Lorem-Ipsum-krzywe.png")

  plt.figure(2)

  plt.subplot(221)
  plt.imshow(imgStraight)
  plt.xticks([])
  plt.yticks([])

  plt.subplot(222)
  plt.imshow(magnitudeSpectrumStraight, cmap="gray")
  plt.xticks([])
  plt.yticks([])

  plt.subplot(223)
  plt.imshow(imgSkew)
  plt.xticks([])
  plt.yticks([])

  plt.subplot(224)
  plt.imshow(magnitudeSpectrumSkew, cmap="gray")
  plt.xticks([])
  plt.yticks([])

  plt.show()

