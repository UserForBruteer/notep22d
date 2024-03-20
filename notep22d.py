import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import sys
import codecs
import json
import os
import importlib
import datetime
import keyboard
import random
import string
import re
from tkinter.colorchooser import askcolor
text_widgets = {}
global font
global bag
global fag
global inbag
font = "arial"
bag = "white"
fag = "black"
inbag = "white"
class PluginAPI:
    def __init__(self, root, tab_control, text_widgets):
        self.root = root
        self.tab_control = tab_control
        self.text_widgets = text_widgets
        self.buttons = {}  # Словарь для хранения информации о кнопках
    def search_word(self, text_widget, word):
        positions = []  # Список для хранения позиций начала и конца каждого найденного слова
        content = text_widget.get("1.0", tk.END)
        pattern = rf"\b{re.escape(word)}\b"  # Используем \b для обозначения границ слова
        matches = re.finditer(pattern, content)
        for match in matches:
            start, end = match.span()
            positions.append((start, end))  # Добавляем позицию начала и конца слова в список
        return positions
    def select_line(self, text_widget, line_number, color):
        # Определите начальный и конечный индексы для выделения всей строки
        start_index = f"{line_number}.0"  # Начало строки
        end_index = f"{line_number + 1}.0"  # Начало следующей строки (не включая конец текущей)
        print(start_index, end_index)
        text_widget.tag_add("search", start_index, end_index)
        text_widget.tag_config("search", background=color)
    def select_word(self, text_widget, start, end, color):
        text_widget.tag_add("search", f"1.0+{start}c", f"1.0+{end}c")
        text_widget.tag_config("search", background=color)
    def choose_color(self):
        color = askcolor()[1]
        if color:
            return color
        return None
    def create_plugin_button(self, name, function, button_id=None):
        button = ttk.Button(root, text=name, command=function)
        button.pack(side=tk.LEFT, padx=5)
        if button_id:  # Если указан ID кнопки, сохраняем информацию о ней
            self.buttons[button_id] = {'button': button, 'name': name, 'function': function}
    def get_button_info(self, button_id):
        return self.buttons.get(button_id)  # Возвращает информацию о кнопке по её ID
    def get_button_ids(self):
        return list(self.buttons.keys())
    def delete_button_by_id(self, button_id):
        button_info = self.buttons.get(button_id)
        if button_info:
            button = button_info['button']
            button.pack_forget()  # Удаляем кнопку из интерфейса
            del self.buttons[button_id]  # Удаляем информацию о кнопке из словаря
    def import_theme(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, 'r') as theme_file:
                theme_data = json.load(theme_file)
            self.apply_theme(theme_data)
    def new_tab(self):
        text = tk.Text(self.tab_control, wrap="word")
        self.tab_control.add(text, text="Untitled")
        self.tab_control.select(text)
        root.deiconify() 
        text.file_path = None
        self.text_widgets[text] = True
        print(text_widgets)
        text.focus_set() 
        self.apply_text_style(text)
    def open_file(self, file_path=None):
        if not file_path:
            file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with codecs.open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            text = tk.Text(self.tab_control, wrap="word")
            text.insert("1.0", content)
            self.tab_control.add(text, text=file_path.split("/")[-1])
            self.tab_control.select(text)
            text.file_path = file_path
            self.text_widgets[text] = True
            self.apply_text_style(text)
    def save_file(self):
        selected_tab = self.tab_control.select()
        if selected_tab:
            text_widget = self.tab_control.nametowidget(selected_tab)
            content = text_widget.get("1.0", tk.END)
            if text_widget.file_path:
                file_path = text_widget.file_path
            else:
                file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if file_path:
                with codecs.open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                text_widget.file_path = file_path
                self.tab_control.tab(selected_tab, text=file_path.split("/")[-1])
    def close_tab(self):
        current_tab = self.tab_control.select()
        if current_tab:
            text_widget = self.tab_control.nametowidget(current_tab)
            self.tab_control.forget(current_tab)
            del self.text_widgets[text_widget]
    def apply_text_style(self, text_widget):
        global font, bag, fag, inbag
        print(text_widget, font, bag, fag, inbag)
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
    def apply_theme(self, theme_data={}):
        if theme_data:
            style = ttk.Style()
            style.theme_use('default')
            length = random.randint(7, 50)
            random_text = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
            style.theme_create(random_text, parent="alt", settings=theme_data)
            style.theme_use(random_text)
            self.root.config(bg=theme_data.get("Root", {}).get("configure", {}).get("background"))
            global font, bag, fag, inbag
            font = theme_data.get("Ttext", {}).get("configure", {}).get("font")
            bag = theme_data.get("Ttext", {}).get("configure", {}).get("bg")
            fag = theme_data.get("Ttext", {}).get("configure", {}).get("fg")
            inbag = theme_data.get("Ttext", {}).get("configure", {}).get("insertbackground")
            for widget in self.text_widgets:
                widget.configure(font=(font, 12))
                widget.configure(bg=bag, fg=fag)
                widget.configure(insertbackground=inbag)
        else:
            style = ttk.Style()
            style.theme_use('default')
    def bind_hotkeys(self):
        keyboard.add_hotkey('Ctrl+N', self.new_tab)
        keyboard.add_hotkey('Ctrl+O', self.open_file)
        keyboard.add_hotkey('Ctrl+S', self.save_file)
        keyboard.add_hotkey('Ctrl+W', self.close_tab)
        keyboard.add_hotkey("Ctrl+C", copy_text)
        keyboard.add_hotkey("Ctrl+V", paste_text)
class PluginManager:
    def __init__(self):
        self.plugins = []
    def load_plugins(self, directory, api):
        directory = os.path.abspath(directory)
        sys.path.append(directory)
        print(f"Loading plugins from {directory}")
        logs_directory = os.path.join(os.path.expanduser('~'), "p22d", "logs")
        os.makedirs(logs_directory, exist_ok=True)
        for filename in os.listdir(directory):
            if filename.endswith(".py"):
                module_name = os.path.splitext(filename)[0]
                try:
                    module = importlib.import_module(module_name)
                    plugin_class = getattr(module, "Plugin")
                    plugin = plugin_class(api)
                    self.plugins.append(plugin)
                    print(f"Plugin '{module_name}' loaded successfully.")
                except Exception as e:
                    error_message = f"Error loading plugin {module_name}: {str(e)}"
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    log_file_path = os.path.join(logs_directory, f"{module_name}_error_{timestamp}.log")
                    with open(log_file_path, 'w') as log_file:
                        log_file.write(error_message)
                    print(f"{module_name} not loaded, log about this error is saved in {log_file_path}")
                    root.update_idletasks()
                    messagebox.showerror("Plugin Error", f"{module_name} not loaded. Log about this error is saved in {log_file_path}")
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
api = PluginAPI(root, tab_control, text_widgets)
if len(sys.argv) > 1:
    file_to_open = sys.argv[1]
    print("File to open:", file_to_open)
    api.open_file(file_to_open)
else:
    api.new_tab()
api.create_plugin_button("New Tab", api.new_tab , button_id="new_tab")
api.create_plugin_button("Open", api.open_file , button_id="open_file")
api.create_plugin_button("Save", api.save_file , button_id="save")
api.create_plugin_button("Close Tab", api.close_tab , button_id="close_tab")
api.create_plugin_button("Import Theme", api.import_theme , button_id="theme")
def load_plugin(plugin_name, api):
    try:
        module = importlib.import_module(plugin_name)
        plugin_class = getattr(module, "Plugin")
        plugin = plugin_class(api)
        print(f"Plugin '{plugin_name}' loaded successfully.")
    except Exception as e:
        error_message = f"Error loading plugin {plugin_name}: {str(e)}"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file_path = os.path.join(logs_directory, f"{plugin_name}_error_{timestamp}.log")
        with open(log_file_path, 'w') as log_file:
            log_file.write(error_message)
        print(f"{plugin_name} not loaded, log about this error is saved in {log_file_path}")
        root.update_idletasks()
        messagebox.showerror("Plugin Error", f"{plugin_name} not loaded. Log about this error is saved in {log_file_path}")
def load_plugins_in_thread(directory, api):
    directory = os.path.abspath(directory)
    sys.path.append(directory)
    print(f"Loading plugins from {directory}")
    logs_directory = os.path.join(os.path.expanduser('~'), "p22d", "logs")
    os.makedirs(logs_directory, exist_ok=True)
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            plugin_name = os.path.splitext(filename)[0]
            plugin_thread = threading.Thread(target=load_plugin, args=(plugin_name, api))
            plugin_thread.start()
plugins_directory = os.path.join(os.path.expanduser('~'), "p22d", "plugins")
plugin_thread = threading.Thread(target=load_plugins_in_thread, args=(plugins_directory, api))
plugin_thread.start()
api.bind_hotkeys()
root.mainloop()
