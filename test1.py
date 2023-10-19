import tkinter as tk
from tkinter import font as tkFont

MAIN_WINDOW_SIZE_X = 400
MAIN_WINDOW_SIZE_Y = 300

class GUIMain(tk.Tk):
    def __init__(self):
        super().__init__()
        self.x = 100
        # FONTS
        self.STANDARD_FONT_1_BOLD = tkFont.Font(family="Arial", size=12, weight='bold')
        self.main_window()

    def main_window(self):
        self.title('TinyFEM')
        self.geometry(f"{MAIN_WINDOW_SIZE_X}x{MAIN_WINDOW_SIZE_Y}")

        button_define_geometry = tk.Button(self, text="DEFINE GEOMETRY", command=self.define_geometry, width=20, height=1)
        button_define_geometry.place(relx=0.025, rely=0.05)

    def define_geometry(self):
        return_geometry = Geometry(self.receive_geometry_value)

    def receive_geometry_value(self, value):
        print("Received value from Geometry:", value)

class Geometry(GUIMain, tk.Toplevel):
    def __init__(self, callback):
        super().__init__()

        # Store the callback function
        self.callback = callback
        self.main_window()

    def main_window(self):
        print(self.x)
        self.title('Define Geometry')
        self.geometry(f"{MAIN_WINDOW_SIZE_X}x{MAIN_WINDOW_SIZE_Y}")

        button_clear = tk.Button(self, text="Geometry", command=self.return_geometry, width=10, height=1)
        button_clear.place(relx=0.025, rely=0.05)

    def return_geometry(self):
        value = 999
        # Call the callback function in the GUI class to pass the value
        self.callback(value)

if __name__ == "__main__":
    app = GUIMain()
    app.mainloop()
