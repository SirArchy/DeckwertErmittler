# Import tkinter library
from tkinter import *

# Create an instance of tkinter window
win = Tk()
win.geometry("700x250")

def open_text():
   text_file = open("test.txt", "r")
   content = text_file.read()
   my_text_box.insert(END, content)
   text_file.close()

def save_text():
   text_file = open("test.txt", "w")
   text_file.write(my_text_box.get(1.0, END))
   text_file.close()

# Creating a text box widget
my_text_box = Text(win, height=10, width=40)
my_text_box.pack()

open_btn = Button(win, text="Open Text File", command=open_text)
open_btn.pack()

# Create a button to save the text
save = Button(win, text="Save File", command=save_text)
save.pack()

win.mainloop()