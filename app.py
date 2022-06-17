from tkinter import *
from tkinter import filedialog
from encrypter import Encrypter
from decrypter import Decrypter
from keys_generator import KeysGenerator
from matplotlib import pyplot
import matplotlib.image as mpimg

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
        self.encryptImage = Button(self.root, text="Encrypt file", pady=5, fg="white", bg="#263D42", command=self.encrypt)
        self.encryptImage.grid(row = 5, columnspan = 4)
        self.decryptImage = Button(self.root, text="Decrypt file", pady=5, fg="white", bg="#263D42", command=self.decrypt)
        self.decryptImage.grid(row = 6, columnspan = 4)
        self.showImages = Button(self.root, text="Show", pady=5, fg="white", bg="#263D42", command=self.show)
        self.showImages.grid(row=7, columnspan=4)
        self.root.mainloop()

    def get_file(self):
        self.main_image = Canvas(self.root, width = 850, height = 400)
        self.filename = filedialog.askopenfilename(initialdir="~/Pictures",
        title = "Select file", filetypes = (("PNG Images", "*.png"), ("PNG Images", "*.PNG")))

    def encrypt(self):
        keys = KeysGenerator()
        keys.generateNewKeys()
        print("Calling encrypter")
        encrypter = Encrypter(self.filename)
        encrypter.encrypt()

    def decrypt(self):
        print("Calling decrypter")
        decrypter = Decrypter(self.filename)
        decrypter.decrypt()

    def show(self):
        path = self.filename.split('/')
        originalFileName = path[len(path) - 1]
        encryptedFileName = "encrypted_test_images/encrypted_" + originalFileName
        decryptedFileName = "decrypted_test_images/decrypted_" + originalFileName
        ecbEncryptedFileName = "encrypted_test_images/ecb_" + originalFileName
        RSAEncryptedFileName = "encrypted_test_images/RSA_encrypted_" + originalFileName
        RSADecryptedFileName = "decrypted_test_images/RSA_decrypted_" + originalFileName

        imgOriginal = mpimg.imread(self.filename)
        imgEncrypted = mpimg.imread(encryptedFileName)
        imgDecrypted = mpimg.imread(decryptedFileName)
        imgEcbEncrypted = mpimg.imread(ecbEncryptedFileName)
        imgRSAEncrypted = mpimg.imread(RSAEncryptedFileName)
        # imgRSADecrypted = mpimg.imread(RSADecryptedFileName)

        pyplot.figure(1)

        pyplot.subplot(231)
        pyplot.imshow(imgOriginal)
        pyplot.title("Original image")
        pyplot.xticks([])
        pyplot.yticks([])

        pyplot.subplot(232)
        pyplot.imshow(imgEncrypted)
        pyplot.title("Encrypted image")
        pyplot.xticks([])
        pyplot.yticks([])

        pyplot.subplot(233)
        pyplot.imshow(imgDecrypted)
        pyplot.title("Decrypted image")
        pyplot.xticks([])
        pyplot.yticks([])

        pyplot.subplot(234)
        pyplot.imshow(imgRSAEncrypted)
        pyplot.title("Built-in RSA encrypted image")
        pyplot.xticks([])
        pyplot.yticks([])

        # pyplot.imshow(236)
        # pyplot.imshow(imgRSADecrypted)
        # pyplot.title("Built-in RSA decrypted image")
        # pyplot.xticks([])
        # pyplot.yticks([])
        
        pyplot.show()

