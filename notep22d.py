import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import sys
def new_tab():
    text = tk.Text(tab_control, wrap="word")
    tab_control.add(text, text="Untitled")
    tab_control.select(text)
    text.file_path = None
    text_widgets[text] = True
    apply_text_style(text)

def open_file(file_path=None):
    if not file_path:
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
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
            # If the text has a file_path attribute, it means it's an existing file that was opened or saved before.
            file_path = text_widget.file_path
        else:
            # If the text doesn't have a file_path attribute, it's a new unsaved tab.
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])

        if file_path:
            with open(file_path, "w") as file:
                file.write(content)
            text_widget.file_path = file_path  # Store the file path for future reference
            tab_control.tab(selected_tab, text=file_path.split("/")[-1])

def close_tab():
    current_tab = tab_control.select()
    if current_tab:
        text_widget = tab_control.nametowidget(current_tab)
        tab_control.forget(current_tab)
        del text_widgets[text_widget]  # Use the text_widget itself as the key

def apply_text_style(text_widget):
    # Define the desired font and other styles here
    text_widget.configure(font=("Helvetica", 12))
    text_widget.configure(bg="white", fg="black")
    text_widget.configure(insertbackground="black")

def apply_theme():
    if len(sys.argv) > 1:
        file_to_open = sys.argv[1]
        print("File to open:", file_to_open)
        open_file(file_to_open)
    else:
        new_tab()
    # Apply custom theme styles to the ttk elements
    theme = {
        "TNotebook": {
            "configure": {
                "background": "#222222",
                "tabmargins": [2, 5, 2, 0],
            },
            "map": {
                "background": [("selected", "#ECECEC")],
            },
        },
        "TNotebook.Tab": {
            "configure": {
                "padding": [10, 5],
                "font": ("Helvetica", 11),
                "background": "#444444",
                "foreground": "white",
            },
            "map": {
                "background": [("selected", "#ECECEC")],
            },
        },
        "TButton": {
            "configure": {
                "font": ("Helvetica", 11),
                "background": "#666666",
                "foreground": "white",
                "relief": tk.FLAT,
                "borderwidth": 0,
                "activebackground": "#888888",
            },
        },
        "TLabel": {
            "configure": {
                "foreground": "white",
                "background": "#222222",
                "font": ("Helvetica", 11),
            },
        },
        "TEntry": {
            "configure": {
                "background": "white",
                "foreground": "black",
                "font": ("Helvetica", 11),
            },
        },
    }

    style = ttk.Style()
    for widget, options in theme.items():
        style.configure(widget, **options)

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


text_widgets = {}


apply_theme()

root.mainloop()
