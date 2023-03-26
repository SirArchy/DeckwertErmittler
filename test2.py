import tkinter as tk
from PIL import Image, ImageTk
import threading
import time

class GifViewer:
    def __init__(self, master, gif_path):
        self.master = master
        self.gif_path = gif_path
        self.gif_frames = []
        self.load_gif_frames()
        self.current_frame = 0
        
        self.canvas = tk.Canvas(self.master, width=300, height=300)
        self.canvas.pack()
        
        self.animate_gif()

    def load_gif_frames(self):
        gif_image = Image.open(self.gif_path)
        try:
            while True:
                gif_frame = gif_image.copy()
                self.gif_frames.append(ImageTk.PhotoImage(gif_frame))
                gif_image.seek(len(self.gif_frames))  # seek to next frame
        except EOFError:
            pass

    def animate_gif(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.gif_frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
        self.master.after(20, self.animate_gif)  # call itself again after 100ms

def show_gif():
    gif_viewer = tk.Toplevel(root)
    gif_viewer.title("Animated Gif Viewer")
    GifViewer(gif_viewer, "loading.gif")
    t = threading.Thread(target=run_function, args=(gif_viewer,))
    t.start()

def run_function(gif_viewer):
    time.sleep(5)  # replace this with your actual function
    gif_viewer.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Window")
    button = tk.Button(root, text="Show Gif", command=lambda: show_gif)
    button.pack()
    root.mainloop()
