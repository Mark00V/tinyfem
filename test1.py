import tkinter as tk
import threading
import time

class YourApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.initialize_ui()

    def initialize_ui(self):
        # Your GUI initialization code here

        create_mesh_button = tk.Button(self, text="Create Mesh", command=self.create_mesh)
        create_mesh_button.pack()

    def create_mesh(self):
        def thread_create_mesh():
            # Your mesh creation code here
            time.sleep(5)  # Simulate mesh creation

        window_create_mesh_wait = tk.Toplevel(self)
        window_create_mesh_wait.title('CREATING MESH')
        window_create_mesh_wait.geometry(f"{350}x{500}")
        window_create_mesh_wait.resizable(False, False)
        window_create_mesh_wait_label = tk.Label(window_create_mesh_wait, text="Creating Mesh...\nPlease Wait",
                                                 font=("Helvetica", 12, "bold"))
        window_create_mesh_wait_label.place(relx=0.25, rely=0.25)

        thread_mesh = threading.Thread(target=thread_create_mesh)
        thread_mesh.start()

        def update_wait_label():
            wait_text = "Creating Mesh...\nPlease Wait"
            while thread_mesh.is_alive():
                wait_text += '.'
                window_create_mesh_wait_label.config(text=wait_text)
                time.sleep(0.2)
            window_create_mesh_wait.destroy()
            print("TEST")

        update_thread = threading.Thread(target=update_wait_label)
        update_thread.start()

if __name__ == "__main__":
    app = YourApp()
    app.mainloop()
