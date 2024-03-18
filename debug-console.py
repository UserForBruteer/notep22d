import tkinter as tk
from tkinter import ttk
from queue import Queue
import threading
import sys

class Console(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Console")

        self.text_widget = tk.Text(self, wrap="word", state="disabled")
        self.text_widget.pack(fill="both", expand=True)

        self.queue = Queue()
        sys.stdout = self

        self.update_console()

    def update_console(self):
        while not self.queue.empty():
            text = self.queue.get()
            self.text_widget.configure(state="normal")
            self.text_widget.insert(tk.END, text)
            self.text_widget.configure(state="disabled")
            self.text_widget.see(tk.END)
        self.after(100, self.update_console)

    def write(self, text):
        self.queue.put(text)

class Plugin:
    def __init__(self, api):
        self.api = api
        api.create_plugin_button("Console", self.open_console)

    def open_console(self):
        self.console = Console(self.api.root)

    def __del__(self):
        sys.stdout = sys.__stdout__  # Восстановим стандартный вывод
