import tkinter as tk
import Buttons as Bt
import Logic as Lg
from pygame import mixer

root = tk.Tk()
mixer.init()
mixer.music.load('xD.mp3')
root.geometry("514x490")
l = Lg.Logic()
board = Bt.Buttons(root, l)
root.mainloop()
