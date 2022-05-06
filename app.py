#!/usr/bin/env python3

#
# Main program
# frontend
#

from tkinter import *
from tkinter import filedialog
from turtle import bgcolor
from PIL import ImageTk, Image
from decoder import Decoder
import fft

class ImageViewer:
    def __init__(self):
        self.root = Tk()
        frame = Frame(self.root)
        frame.grid()
        self.root.geometry("850x800")
        self.root.title("Projekt E-Media")
        
        #Canvasses
        self.main_image = Canvas(self.root, width = 850, height = 400, bg = 'white')
        self.main_image.grid(row = 0, column = 0, rowspan = 3, columnspan = 4 )
        self.pixels_info = Canvas(self.root, width = 100, height = 200)
        self.pixels_info.grid(row = 3, column = 0, sticky = W)
        self.header_info = Canvas(self.root, width = 100, height = 200)
        self.header_info.grid(row = 3, column = 1)
        self.size_info = Canvas(self.root, width = 100, height = 200)
        self.size_info.grid(row = 3, column = 2)
        self.chunks_info = Canvas(self.root, width = 100, height = 200)
        self.chunks_info.grid(row = 3, column = 3)

        #Buttons
        self.addFile = Button(self.root, text="Open file",pady=5, fg="white", bg="#263D42", command=self.get_file)
        self.addFile.grid(row = 4, columnspan = 4)
        self.checkFFT = Button(self.root, text="Check FFT", pady=5, fg="white", bg="#263D42", command=self.check)
        self.checkFFT.grid(row = 5, columnspan = 4)

        self.root.mainloop()

    def get_file(self):
        self.main_image = Canvas(self.root, width = 850, height = 400)
        self.filename = filedialog.askopenfilename(initialdir="~/Pictures",
        title = "Select file", filetypes = (("PNG Images", "*.png"), ("PNG Images", "*.PNG")))

        decoder = Decoder(self.filename)
        decoder.decode()
        width, height, bit_depth, color_type, compr_type, filter_type, interl_type, normal_image_size, reduced_image_size, critical_chunks, ancillary_chunks = decoder.header_info()
        self.pixels_info.destroy()
        self.header_info.destroy()
        self.size_info.destroy()
        self.chunks_info.destroy()

        self.pixels_info = Canvas(self.root, width = 100, height = 200)
        self.pixels_info.grid(row = 3, column = 0)
        self.header_info = Canvas(self.root, width = 100, height = 200)
        self.header_info.grid(row = 3, column = 1)
        self.size_info = Canvas(self.root, width = 100, height = 200)
        self.size_info.grid(row = 3, column = 2)
        self.chunks_info = Canvas(self.root, width = 100, height = 200)
        self.chunks_info.grid(row = 4, column = 0)

        Label(self.pixels_info, text="Width: " + str(width)).grid()
        Label(self.pixels_info, text="Height: " + str(height)).grid()
        Label(self.header_info, text="Bit depth: " + str(bit_depth)).grid()
        Label(self.header_info, text="Color type: " + str(color_type)).grid()
        Label(self.header_info, text="Compression type: " + str(compr_type)).grid()
        Label(self.header_info, text="Filter type: " + str(filter_type)).grid()
        Label(self.header_info, text="Interline type: " + str(interl_type)).grid()
        Label(self.size_info, text="Normal image size (bytes): " + str(normal_image_size)).grid()
        Label(self.size_info, text="Reduced image size (bytes): " + str(reduced_image_size)).grid()
        Label(self.chunks_info, text="Critical chunks: ").grid()
        for i in critical_chunks:
            Label(self.chunks_info, text=str(i)).grid()
        Label(self.chunks_info, text="Ancillary chunks: ").grid()
        for i in ancillary_chunks:
            Label(self.chunks_info, text=str(i)).grid()

        fft.display(self.filename)
        decoder.make_reduced_image(self.filename)

        im = Image.open(self.filename)
        newsize = (850, 400)
        im = im.resize(newsize)
        im.save("test_images/copy.png")
        img = PhotoImage(Image.open("test_images/copy.png"))     
        self.main_image.create_image(0,0,anchor = 'nw',image = img)
        self.main_image.grid(row = 0, column = 0, rowspan = 3, columnspan = 3 )
        self.main_image = img

    def check(self):
        fft.checkFFT()

