import tkinter as tk

def on_greet():
    # Get the name from the entry field
    name = name_entry.get()

    # Update the label with the greeting
    greeting_label.config(text=f"Hello, {name}!")

# Create the main window
root = tk.Tk()
root.title("Tkinter Demo")

# Create a label widget
greeting_label = tk.Label(root, text="Enter your name and click the button to be greeted!")
greeting_label.pack()

# Create an entry widget
name_entry = tk.Entry(root)
name_entry.pack()

# Create a button widget
greet_button = tk.Button(root, text="Greet", command=on_greet)
greet_button.pack()

# Start the GUI event loop
root.mainloop()
