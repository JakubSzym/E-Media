#
# class Driver
# frontend
#

from tkinter import filedialog, Label

class Driver:
  def __init__(self, root):
    self.files = []
    self.root = root

  def addFile(self):
    for widget in self.root.winfo_children():
      widget.destroy()

    filename = filedialog.askopenfilename(initialdir="~/Projects", title="Select file",
    filetypes=(("PNG Images", "*.png"), ("PNG Images", "*.PNG")))
    self.files.append(filename)

    for file in self.files:
      label = Label(self.root, text=file, bg="gray")
      label.pack()

