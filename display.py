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