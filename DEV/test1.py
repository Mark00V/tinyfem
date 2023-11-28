##############################################################
# implement timer where useful
import time

class TimerContextManager:
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.time()
        elapsed_time = self.end_time - self.start_time
        print(f"Time elapsed: {elapsed_time} seconds")

# Usage:
with TimerContextManager():
    # Code block to measure execution time
    for _ in range(1000000):
        pass

# and

class ExceptionHandler:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"Exception type: {exc_type}")
            print(f"Exception value: {exc_value}")
            print("Handling the exception here.")
            # You can choose to suppress the exception by returning True.
            return True
        # If no exception occurred, __exit__ can return None or False to propagate.
        return False

# Usage:
with ExceptionHandler():
    # Code block that may raise an exception
    x = 1 / 0  # This will raise a ZeroDivisionError

##############################################################
# Implement progress bar:
import tkinter as tk
from tkinter import ttk
from tqdm import tqdm
import threading
import time

def long_running_task(progress_bar):
    for _ in tqdm(range(100), desc="Processing"):
        time.sleep(0.1)
        progress_bar["value"] += 1
    progress_bar.stop()

def start_task():
    progress_bar.start()
    threading.Thread(target=long_running_task, args=(progress_bar,)).start()

app = tk.Tk()
app.title("Tkinter with tqdm")

progress_bar = ttk.Progressbar(app, length=200, mode="determinate")
progress_bar.pack(pady=10)

start_button = tk.Button(app, text="Start Task", command=start_task)
start_button.pack()

app.mainloop()