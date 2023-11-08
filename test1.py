from PIL import Image
import pytesseract

# Open an image using Pillow (PIL)
image = Image.open("tiny_fem_icon.ico")

# Perform OCR using pytesseract
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)


############################

from PIL import Image
import io

# Assuming 'byte_data' contains your byte sequence
byte_data = b'\x89PNG\r\n...'

# Create an image from the byte sequence
img = Image.open(io.BytesIO(byte_data))

# Save the image as a PNG file
img.save("icon.png", "PNG")

###########################

import tkinter as tk

root = tk.Tk()
root.title("My App")

# Load the image as an icon
icon_image = tk.PhotoImage(file="icon.png")

# Set the icon for the tkinter window
root.tk.call('wm', 'iconphoto', root._w, icon_image)

# Rest of your tkinter application code here

root.mainloop()