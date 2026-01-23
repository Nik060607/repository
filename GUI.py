import tkinter as tk
from tkinter import ttk, messagebox

# Инициализация окна
win = tk.Tk()
win.title("Контроль светодиодов")
win.resizable(True, True)  # разрешаем изменение размеров окна

# Настраиваем стили
style = ttk.Style()
style.theme_use('clam')  # современный стиль

# Центральная рамка для элементов
frame = ttk.Frame(win, padding="10")
frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

# Настройка растяжимости окна
win.columnconfigure(0, weight=1)
win.rowconfigure(0, weight=1)

# Поля ввода и шкала яркости
LED_time_entry = ttk.Entry(frame, width=10)
LED_time_entry.grid(column=1, row=1, sticky=tk.W)

ttk.Label(frame, text="Время включения (сек.)").grid(column=2, row=1, sticky=tk.W)

LED_brightness_slider = ttk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL)
LED_brightness_slider.set(50)  # начальное значение
LED_brightness_slider.grid(column=1, row=2, columnspan=2, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Яркость LED:").grid(column=1, row=3, sticky=tk.W)

# Функциональные кнопки
def led_on():
    brightness = LED_brightness_slider.get()
    delay = int(LED_time_entry.get())
    print(f"LED включен на {delay} секунд с яркостью {brightness}%")

def led_off():
    print("LED выключен")

def blue_led():
    print("Blue LED активирован")

def red_led():
    print("Red LED активирован")

def about_message():
    messagebox.showinfo("О программе", "Программное обеспечение для управления LED\nВерсия 1.0\nЯнварь 2026")

# Кнопки управления
blue_btn = ttk.Button(frame, text="Blue LED", command=blue_led)
blue_btn.grid(column=1, row=4, sticky=tk.W)

red_btn = ttk.Button(frame, text="Red LED", command=red_led)
red_btn.grid(column=2, row=4, sticky=tk.W)

about_btn = ttk.Button(frame, text="Справка", command=about_message)
about_btn.grid(column=1, row=5, sticky=tk.W)

quit_btn = ttk.Button(frame, text="Закрыть", command=win.destroy)
quit_btn.grid(column=2, row=5, sticky=tk.W)

# Дополнительные кнопки управления
on_btn = ttk.Button(frame, text="LED ВКЛ", command=led_on)
on_btn.grid(column=3, row=1, sticky=tk.W)

off_btn = ttk.Button(frame, text="LED ВЫКЛ", command=led_off)
off_btn.grid(column=3, row=2, sticky=tk.W)

# Отступы и выравнивания
for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

# Запускаем основное окно
win.mainloop()
