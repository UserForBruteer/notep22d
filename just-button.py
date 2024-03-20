import tkinter as tk
from tkinter import ttk

class Plugin:
    def __init__(self, api):
        self.api = api
        api.create_plugin_button("Button", self.on_button_click, button_id="plugin_button")

    def on_button_click(self):
        print("Plugin Button Clicked!")
