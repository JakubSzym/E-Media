#
# class Driver
# frontend
#

from tkinter import filedialog, Label
from PIL import Image,ImageTk
from decoder import Decoder

class Driver:
  def __init__(self, root):
    self.files = []
    self.root = root

  def addFile(self):
    filename = filedialog.askopenfilename(initialdir="~/Projects",
    title="Select file",filetypes=(("PNG Images", "*.png"), ("PNG Images", "*.PNG")))
    self.files.append(filename)
    decoder = Decoder(filename)
    decoder.decode()
    decoder.header_info()

    for file in self.files:
      photo_file = Image.open(file)
      photo_file = photo_file.resize((600, 600),Image.ANTIALIAS)
      photo = ImageTk.PhotoImage(photo_file)
      label = Label(self.root, image=photo)
      label.image=photo
      label.grid()
