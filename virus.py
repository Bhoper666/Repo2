import tkinter as tk
from tkinter import messagebox
import os
import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

root = tk.Tk()
root.title('')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(screensize)


print(screen_width + screen_height)
print(screensize)

root.mainloop()
