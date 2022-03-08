#!/usr/bin/env python3

#
# Main program
# frontend
#

from tkinter import *

from driver import Driver

root = Tk()

root.title("Projekt E-Media")

canvas = Canvas(root, height=700, width=700, bg="#263D42")
canvas.pack()

frame = Frame(root, bg="white")

driver = Driver(frame)

driver.root.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

addFile = Button(root, text="Open file", padx=10, pady=5, fg="white", bg="#263D42", command=driver.addFile)
addFile.pack()

root.mainloop()