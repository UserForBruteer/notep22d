import tkinter as tk
from tkinter import ttk
from queue import Queue
import threading
import sys
import re
import time

class Plugin:
    def __init__(self, api):
        self.api = api
        word_to_search = "p22d"
        color = self.api.choose_color()
        while True:
            for text_widget in api.text_widgets.keys():
                matches = api.search_word(text_widget, word_to_search)
                print(f"Found {len(matches)} occurrences of the word '{word_to_search}'.")
                if len(matches) == 0:
                    text_widget.tag_remove("search", "1.0", tk.END)
                    time.sleep(1)
                    break
                for start, end in matches:
                    print(start, end)
                    self.api.select_word(text_widget, start, end, color)
            time.sleep(0.1)
