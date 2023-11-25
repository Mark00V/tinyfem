import tkinter as tk
from tkinter import PhotoImage

root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Specify the complete path to the image
image = PhotoImage(file="../Supp/demo_gui.png")

# Create the image item on the canvas
canvas.create_image(0, 0, anchor=tk.NW, image=image)

root.mainloop()
