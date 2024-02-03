import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import sys
import codecs
import keyboard
import json
import random
import string
import os
import importlib
import datetime
username = os.getlogin()
data_dir = f"C://Users//{username}//p22d"
if not os.path.exists(data_dir):
    sys.path.append(data_dir)
class PluginManager:
    def __init__(self):
        self.plugins = []

    def load_plugins(self, directory, **kwargs):
        directory = os.path.abspath(directory)
        sys.path.append(directory)
        print(f"Loading plugins from {directory}")

        logs_directory = f"C://Users//{username}//p22d//logs"
        if not os.path.exists(logs_directory):
            os.makedirs(logs_directory)

        for filename in os.listdir(directory):
            if filename.endswith(".py"):
                module_name = os.path.splitext(filename)[0]
                try:
                    module = importlib.import_module(module_name)
                    plugin_class = getattr(module, "Plugin")
                    plugin = plugin_class()
                    self.plugins.append(plugin)
                    print(f"Plugin '{module_name}' loaded successfully.")
                    plugin.execute(**kwargs)
                except Exception as e:
                    error_message = f"Error loading plugin {module_name}: {str(e)}"
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    log_file_path = os.path.join(logs_directory, f"{module_name}_error_{timestamp}.log")
                    with open(log_file_path, 'w') as log_file:
                        log_file.write(error_message)
                    print(f"{module_name} not loaded, log about this error is saved in {log_file_path}")

                    messagebox.showerror("Plugin Error", f"{module_name} not loaded. Log about this error is saved in {log_file_path}")


class PluginData:
    def __init__(self, root, tab_control):
        self.root = root
        self.tab_control = tab_control

text_widgets = {}
global font
global bag
global fag
global inbag
font = "arial"
bag = "white"
fag = "black"
inbag = "white"
def import_theme():
    file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, 'r') as theme_file:
            theme_data = json.load(theme_file)
            apply_theme(theme_data)

def new_tab():
    text = tk.Text(tab_control, wrap="word")
    tab_control.add(text, text="Untitled")
    tab_control.select(text)
    text.file_path = None
    text_widgets[text] = True
    print(text)
    apply_text_style(text)


def open_file(file_path=None):
    if not file_path:
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with codecs.open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        text = tk.Text(tab_control, wrap="word")
        text.insert("1.0", content)
        tab_control.add(text, text=file_path.split("/")[-1])
        tab_control.select(text)
        text.file_path = file_path
        text_widgets[text] = True
        apply_text_style(text)

def save_file():
    selected_tab = tab_control.select()
    if selected_tab:
        text_widget = tab_control.nametowidget(selected_tab)
        content = text_widget.get("1.0", tk.END)

        if text_widget.file_path:
            file_path = text_widget.file_path
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])

        if file_path:
            with codecs.open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            text_widget.file_path = file_path
            tab_control.tab(selected_tab, text=file_path.split("/")[-1])

def close_tab():
    current_tab = tab_control.select()
    if current_tab:
        text_widget = tab_control.nametowidget(current_tab)
        tab_control.forget(current_tab)
        del text_widgets[text_widget] 

def apply_text_style(text_widget):
    global font, bag, fag, inbag

    text_widget.configure(font=(font, 12))
    text_widget.configure(bg=bag, fg=fag)
    text_widget.configure(insertbackground=inbag)

    text_widget.tag_configure("sel", background=fag, foreground=bag)
    text_widget.configure(selectbackground=fag, selectforeground=bag)

    def select_word(event):
        text_widget.tag_remove("sel", "1.0", tk.END)
        text_widget.tag_add("sel", "insert wordstart", "insert wordend+1c")
    
    text_widget.bind("<Double-Button-1>", select_word)
    print(f"add style to {text_widget}")


def apply_theme(theme_data=None):
    if theme_data:
        style = ttk.Style()

        # Сброс темы к значению по умолчанию
        style.theme_use('default')

        length = random.randint(7, 50)
        random_text = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
        style.theme_create(random_text, parent="alt", settings=theme_data)
        style.theme_use(random_text)

        root.config(bg=theme_data.get("Root", {}).get("configure", {}).get("background"))

        global font, bag, fag, inbag
        font = theme_data.get("Ttext", {}).get("configure", {}).get("font")
        bag = theme_data.get("Ttext", {}).get("configure", {}).get("bg")
        fag = theme_data.get("Ttext", {}).get("configure", {}).get("fg")
        inbag = theme_data.get("Ttext", {}).get("configure", {}).get("insertbackground")

        # Применение стиля ко всем виджетам текста в Notebook
        for widget in text_widgets:
            widget.configure(font=(font, 12))
            widget.configure(bg=bag, fg=fag)
            widget.configure(insertbackground=inbag)

def copy_text():
    widget = root.focus_get()
    if isinstance(widget, tk.Text):
        text = widget.get("sel.first", "sel.last")
        widget.clipboard_clear()
        widget.clipboard_append(text)

def paste_text():
    widget = root.focus_get()
    if isinstance(widget, tk.Text):
        text = widget.clipboard_get()
        widget.insert("insert", text)


root = tk.Tk()
root.title("notep22d")
tab_control = ttk.Notebook(root)
tab_control.pack(fill="both", expand=True)
if len(sys.argv) > 1:
    file_to_open = sys.argv[1]
    print("File to open:", file_to_open)
    open_file(file_to_open)
else:
    new_tab()
new_tab_button = ttk.Button(root, text="New Tab", command=new_tab)
new_tab_button.pack(side=tk.LEFT, padx=5)

open_button = ttk.Button(root, text="Open", command=open_file)
open_button.pack(side=tk.LEFT, padx=5)

save_button = ttk.Button(root, text="Save", command=save_file)
save_button.pack(side=tk.LEFT, padx=5)

close_tab_button = ttk.Button(root, text="Close Tab", command=close_tab)
close_tab_button.pack(side=tk.LEFT, padx=5)

import_theme_button = ttk.Button(root, text="Import Theme", command=import_theme)
import_theme_button.pack(side=tk.LEFT, padx=5)


def bind_hotkeys():
    keyboard.add_hotkey('Ctrl+N', new_tab)
    keyboard.add_hotkey('Ctrl+O', open_file)
    keyboard.add_hotkey('Ctrl+S', save_file)
    keyboard.add_hotkey('Ctrl+W', close_tab)
    keyboard.add_hotkey("Ctrl+C", copy_text)
    keyboard.add_hotkey("Ctrl+V", paste_text)


plugins_directory = f"C://Users//{username}//p22d//plugins"
if not os.path.exists(plugins_directory):
    os.makedirs(plugins_directory)
plugins_directory = f"C://Users//{username}//p22d//plugins"
plugin_manager = PluginManager()
plugin_manager.load_plugins(directory=f"C://Users//{username}//p22d//plugins", root=root, tab_control=tab_control, text_widgets=text_widgets)
apply_theme()
bind_hotkeys()

root.mainloop()
