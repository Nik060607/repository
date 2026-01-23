import tkinter as tk
from tkinter import ttk

# Инициализация окна
win = tk.Tk()
win.title("Пример красной кнопки")
win.geometry("200x100")

# Центрирование содержимого
frame = ttk.Frame(win, padding="10")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Текст над кнопкой
label = ttk.Label(frame, text="Нажмите красную кнопку!")
label.pack(pady=10)

# Логика кнопки
def on_button_click():
    print("Красная кнопка нажата!")

# Красная кнопка
red_button = ttk.Button(
    frame,
    text="Красный!",
    style="Red.TButton",
    command=on_button_click
)
red_button.pack(pady=10)

# Настройка красного стиля кнопки
style = ttk.Style()
style.configure("Red.TButton", background="red", foreground="white", font=("Arial", 14))

# Запускаем основное окно
win.mainloop()
