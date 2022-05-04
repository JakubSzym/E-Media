#
# class Driver
# frontend
#

from tkinter import Label, filedialog
from decoder import Decoder
from cv2 import *
from display import display, checkFFT

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
    width, height, bit_depth, color_type, compr_type, filter_type, interl_type, normal_image_size, reduced_image_size = decoder.header_info()
    
    for widget in self.root.winfo_children():
      widget.destroy()

    Label(self.root, text="Width: " + str(width)).pack()
    Label(self.root, text="Height: " + str(height)).pack()
    Label(self.root, text="Bit depth: " + str(bit_depth)).pack()
    Label(self.root, text="Color type: " + str(color_type)).pack()
    Label(self.root, text="Compression type: " + str(compr_type)).pack()
    Label(self.root, text="Filter type: " + str(filter_type)).pack()
    Label(self.root, text="Interline type: " + str(interl_type)).pack()
    Label(self.root, text="Normal image size (bytes): " + str(normal_image_size)).pack()
    Label(self.root, text="Reduced image size (bytes): " + str(reduced_image_size)).pack()

    decoder.make_reduced_image(filename)
    display(filename)

  def check(self):
    checkFFT()
