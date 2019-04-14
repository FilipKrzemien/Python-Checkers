import tkinter as tk
import buttons as Bt
import logic as Lg

root = tk.Tk()
root.geometry("514x490")
logic = Lg.Logic()
board = Bt.Buttons(root, logic)
root.mainloop()
