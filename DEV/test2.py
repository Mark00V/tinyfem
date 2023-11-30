import tkinter as tk

# Create the main window
root = tk.Tk()
root.geometry("300x200")

# Create a Label widget with text
label = tk.Label(root, text="This is a left-anchored label\nTest next line\nTest third line", anchor="w", justify="left")
label.place(relx=0.01, rely=0.01)

# Start the Tkinter main loop
root.mainloop()
