import tkinter as tk
from tkinter import ttk

# Основная программа
window = tk.Tk()
window.title("Выбор плат Arduino")

# Темы
style = ttk.Style()
style.theme_use('clam')

# Виджет Label
label = ttk.Label(window, text="Ваш выбор:")
label.pack(pady=10)

# Progress bar
progress = ttk.Progressbar(window, orient="horizontal", length=200, mode="indeterminate")
progress.pack(pady=10)
progress.start()

# Combobox
combo_var = tk.StringVar()
combobox = ttk.Combobox(window, values=["Arduino Uno", "Arduino NanoATMega328"], state="readonly", textvariable=combo_var)
combobox.pack(pady=10)

# Реакция на выбор
def on_select(event):
    selected_value = combo_var.get()
    label.config(text=f"Ваш выбор: {selected_value}")

combobox.bind("<<ComboboxSelected>>", on_select)

# Проверочный элемент (Checkbutton)
check_var = tk.BooleanVar(value=False)
checkbox = ttk.Checkbutton(window, text="Активировать", variable=check_var)
checkbox.pack(pady=10)

# Иконка на кнопке
btn_icon = tk.PhotoImage(file="Arduino.png").subsample(5, 5)
button = ttk.Button(window, text="Подтвердить", image=btn_icon, compound=tk.LEFT)
button.pack(pady=35)

# Запуск основной петли
window.mainloop()