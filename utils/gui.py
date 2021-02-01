from tkinter import *


def run_gui():
    root = Tk()
    root.eval('tk::PlaceWindow . center')

    label1 = Label(root, text="Welcome to the Martrec GUI!")
    label1.pack()

    label2 = Label(root, text="Click the Button Below to Start")
    label2.pack()

    root.mainloop()
