import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import sys
import codecs
import keyboard
import json
import random
import string
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

# В функции open_file:
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

# В функции save_file:
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
        del text_widgets[text_widget]  # Use the text_widget itself as the key

def apply_text_style(text_widget):
    global font, bag, fag, inbag
    # Определение желаемого шрифта и других стилей здесь
    text_widget.configure(font=(font, 12))
    text_widget.configure(bg=bag, fg=fag)
    text_widget.configure(insertbackground=inbag)

    # Добавление стилей для выделенного текста
    text_widget.tag_configure("sel", background=fag, foreground=bag)
    text_widget.configure(selectbackground=fag, selectforeground=bag)

    # Обработчик для двойного щелчка мыши
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

text_widgets = {}

def bind_hotkeys():
    keyboard.add_hotkey('Ctrl+N', new_tab)
    keyboard.add_hotkey('Ctrl+O', open_file)
    keyboard.add_hotkey('Ctrl+S', save_file)
    keyboard.add_hotkey('Ctrl+W', close_tab)
    keyboard.add_hotkey("Ctrl+C", copy_text)
    keyboard.add_hotkey("Ctrl+V", paste_text)



apply_theme() # Default theme
new_tab()
bind_hotkeys()

root.mainloop()
