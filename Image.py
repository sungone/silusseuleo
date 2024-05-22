from tkinter import *
from PIL import Image, ImageTk
import requests


class mapImage:
    def __init__(self, filename, window):
        self.filename = filename
        self.window = window

        img = None
        img = PhotoImage(file=self.filename)
        iLabel = Label(self.window, image=img)
        iLabel.image = img
        iLabel.pack()
