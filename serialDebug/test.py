import tkinter as tk
from tkinter import ttk
import threading


POLLING_DELAY = 250  # ms
lock = threading.Lock()  # Lock for shared resources.
finished = False

root = tk.Tk()
label = tk.Label(text='vinoth')
label.pack()

def fix():
    global finished

    with lock:
        finished = False
    t = threading.Thread(target=count)
    t.daemon = True
    root.after(POLLING_DELAY, check_status)  # Start polling.
    t.start()

def check_status():
    with lock:
        if not finished:
            root.after(POLLING_DELAY, check_status)  # Keep polling.
        else:
            print('end')

def count():
    global finished

    for i in range(88888):
        a = i
    with lock:
        finished = True
        label['text'] = a


button = tk.Button(text='sub', command=fix)
button.pack()
dropdown = ttk.Combobox()
dropdown.pack()

root.mainloop()