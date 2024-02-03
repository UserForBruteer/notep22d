import tkinter as tk
from tkinter import ttk

class Plugin:
    def execute(self, **kwargs):
        self.root = kwargs.get('root')
        self.tab_control = kwargs.get('tab_control')
        self.add_button()

    def add_button(self):
        new_button = ttk.Button(self.root, text="Plugin Button", command=self.on_button_click)
        new_button.pack(side=tk.LEFT, padx=5)

    def on_button_click(self):
        print("Plugin Button Clicked!")
