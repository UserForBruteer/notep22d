import tkinter as tk
from tkinter import ttk
import sys
import time

class Plugin:
    def execute(self, **kwargs):
        self.root = kwargs.get('root')
        self.tab_control = kwargs.get('tab_control')

        # Создаем кнопку "Check Debug"
        debug_button = ttk.Button(self.root, text="Check Debug", command=lambda: self.show_debug(self.root))
        debug_button.pack(side=tk.LEFT, padx=5)

    def show_debug(self, root):
        # Создаем новое окно для отображения содержимого консоли
        debug_window = tk.Toplevel(root)
        debug_window.title("Debug Window")

        # Текстовое поле для отображения содержимого консоли
        console_text = tk.Text(debug_window, wrap="word")
        console_text.pack(expand=True, fill="both")

        # Перехватываем поток вывода и выводим его в текстовое поле
        class ConsoleRedirector:
            def write(self, message):
                console_text.insert(tk.END, message)
                console_text.yview(tk.END)

        sys.stdout = ConsoleRedirector()

        # Выводим сообщение в консоль для тестирования
        print("Debug information...")

if __name__ == "__main__":
    # При запуске файла напрямую можно выполнить тестовый пример
    root = tk.Tk()
    root.title("Test Debug Plugin")
    tab_control = ttk.Notebook(root)
    tab_control.pack(fill="both", expand=True)

    plugin = DebugPlugin()
    plugin.execute(root=root, tab_control=tab_control)

    root.mainloop()
