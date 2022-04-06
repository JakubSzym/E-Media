#
# class Driver
# frontend
#

from tkinter import filedialog
#from PIL import Image
from decoder import Decoder
from cv2 import *
from display import display

class Driver:
  def __init__(self, root):
    self.files = []
    self.root = root

  def addFile(self):
    filename = filedialog.askopenfilename(initialdir="~/Pictures",
    title="Select file",filetypes=(("PNG Images", "*.png"), ("PNG Images", "*.PNG")))
    self.files.append(filename)
    decoder = Decoder(filename)
    decoder.decode()
    
    display(filename)
