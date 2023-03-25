import tkinter as tk
import time
from gifplayer import PhotoImagePlayer

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pop-up Message")

        # Create pop-up message
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Function Running")
        self.popup_label = tk.Label(self.popup, text="Function is running...")
        self.popup_animation = PhotoImagePlayer(self.popup)
        self.popup_label.pack(pady=10)
        self.popup_animation.pack(pady=10)
        self.popup_animation.load('loading.gif')
        self.popup.withdraw()  # Hide the popup initially
        

        # Create button to trigger function
        self.button = tk.Button(self.root, text="Run Function", command=self.run_function)
        self.button.pack(pady=10)


    def run_function(self):
        # Show the pop-up message
        self.popup.deiconify()
        self.popup.grab_set()
        self.popup_animation.load('loading.gif')
        self.popup.update()
        # Call your function here
        time.sleep(10) 
        self.popup.withdraw()
        self.popup.grab_release()

    def start(self):    
        self.root.mainloop()


app = App()
app.start()
