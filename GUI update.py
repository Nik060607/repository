import tkinter as tk
from tkinter import ttk, messagebox

# Инициализация окна
win = tk.Tk()
win.title("Контроль светодиодов")
win.resizable(True, True)
win.configure(bg='#2b2b2b')  # Темный фон окна

# Настраиваем стили
style = ttk.Style()
style.theme_use('clam')

# Современные цвета
bg_color = '#2b2b2b'
frame_bg = '#3c3c3c'
text_color = '#e0e0e0'
accent_color = '#808080'
button_bg = '#404040'
button_active = '#505050'

# Конфигурация стилей
style.configure('Custom.TFrame', background=frame_bg)
style.configure('Title.TLabel', 
                font=('Segoe UI', 14, 'bold'),
                foreground=accent_color,
                background=bg_color)
style.configure('Custom.TLabel',
                font=('Segoe UI', 10),
                foreground=text_color,
                background=frame_bg)
style.configure('Custom.TButton',
                font=('Segoe UI', 10),
                background=button_bg,
                foreground=text_color,
                borderwidth=1,
                relief='flat')
style.map('Custom.TButton',
          background=[('active', button_active)],
          relief=[('pressed', 'sunken')])
style.configure('Custom.TEntry',
                fieldbackground='#4a4a4a',
                foreground=text_color,
                insertcolor=text_color)
style.configure('Horizontal.TScale',
                background=frame_bg,
                troughcolor='#4a4a4a')

# Заголовочная панель с кружочками
header_frame = tk.Frame(win, bg=bg_color, height=40)
header_frame.pack(fill=tk.X, padx=10, pady=(10, 0))

# Создаем круглые индикаторы
circle_frame = tk.Frame(header_frame, bg=bg_color)
circle_frame.pack(side=tk.LEFT, padx=(0, 20))

# Красный кружок
red_circle = tk.Canvas(circle_frame, width=20, height=20, bg=bg_color, highlightthickness=0)
red_circle.create_oval(2, 2, 18, 18, fill='red', outline='black', width=2)
red_circle.pack(side=tk.LEFT, padx=2)

# Желтый кружок
yellow_circle = tk.Canvas(circle_frame, width=20, height=20, bg=bg_color, highlightthickness=0)
yellow_circle.create_oval(2, 2, 18, 18, fill='yellow', outline='black', width=2)
yellow_circle.pack(side=tk.LEFT, padx=2)

# Зеленый кружок
green_circle = tk.Canvas(circle_frame, width=20, height=20, bg=bg_color, highlightthickness=0)
green_circle.create_oval(2, 2, 18, 18, fill='green', outline='black', width=2)
green_circle.pack(side=tk.LEFT, padx=2)

# Заголовок Dimmer LED
title_label = tk.Label(header_frame,
                      text="Dimmer LED",
                      font=('Segoe UI', 16, 'bold'),
                      fg=accent_color,
                      bg=bg_color)
title_label.pack(side=tk.LEFT)

# Центральная рамка для элементов
frame = ttk.Frame(win, style='Custom.TFrame', padding="20")
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Функции для анимации кружочков
def animate_circles():
    """Анимация переключения кружочков"""
    colors = ['red', 'yellow', 'green']
    current_color = red_circle.itemcget(1, 'fill')
    next_color = colors[(colors.index(current_color) + 1) % 3]
    
    # Сбрасываем все кружки
    red_circle.itemconfig(1, fill='red' if next_color == 'red' else 'darkred')
    yellow_circle.itemconfig(1, fill='yellow' if next_color == 'yellow' else 'darkgoldenrod')
    green_circle.itemconfig(1, fill='green' if next_color == 'green' else 'darkgreen')
    
    win.after(1000, animate_circles)  # Анимация каждую секунду

# Поля ввода и шкала яркости с метками
ttk.Label(frame, text="Время включения (сек.):", style='Custom.TLabel').grid(column=0, row=0, sticky=tk.W, pady=(0, 10))

LED_time_entry = ttk.Entry(frame, width=15, style='Custom.TEntry')
LED_time_entry.insert(0, "5")  # Значение по умолчанию
LED_time_entry.grid(column=1, row=0, sticky=tk.W, padx=(10, 20), pady=(0, 10))

ttk.Label(frame, text="Яркость LED:", style='Custom.TLabel').grid(column=0, row=1, sticky=tk.W, pady=(0, 10))

# Фрейм для слайдера и значения
slider_frame = ttk.Frame(frame, style='Custom.TFrame')
slider_frame.grid(column=1, row=1, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

LED_brightness_slider = ttk.Scale(slider_frame, from_=0, to=100, orient=tk.HORIZONTAL, style='Horizontal.TScale')
LED_brightness_slider.set(50)
LED_brightness_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Отображение текущего значения слайдера
brightness_value = tk.StringVar(value="50%")
brightness_label = ttk.Label(slider_frame, 
                            textvariable=brightness_value, 
                            style='Custom.TLabel',
                            width=5)
brightness_label.pack(side=tk.LEFT, padx=(10, 0))

def update_brightness_label(event=None):
    """Обновление значения яркости"""
    value = int(LED_brightness_slider.get())
    brightness_value.set(f"{value}%")

LED_brightness_slider.configure(command=update_brightness_label)

# Основные функциональные кнопки
def led_on():
    brightness = LED_brightness_slider.get()
    delay = LED_time_entry.get()
    try:
        delay = int(delay)
        messagebox.showinfo("LED Включен", 
                           f"LED включен на {delay} секунд с яркостью {brightness}%",
                           parent=win)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное число секунд", parent=win)

def led_off():
    messagebox.showinfo("LED Выключен", "LED выключен", parent=win)

def blue_led():
    messagebox.showinfo("Blue LED", "Blue LED активирован", parent=win)

def red_led():
    messagebox.showinfo("Red LED", "Red LED активирован", parent=win)

def about_message():
    messagebox.showinfo("О программе", 
                       "Программное обеспечение для управления LED\n\n"
                       "Версия 2.0\n"
                       "Январь 2026\n\n"
                       "© Все права защищены",
                       parent=win)

# Секция основных кнопок управления
buttons_frame = ttk.Frame(frame, style='Custom.TFrame')
buttons_frame.grid(column=0, row=2, columnspan=4, pady=(20, 0))

# Первая строка кнопок
on_btn = ttk.Button(buttons_frame, text="LED ВКЛ", command=led_on, style='Custom.TButton', width=12)
on_btn.grid(column=0, row=0, padx=5, pady=5)

off_btn = ttk.Button(buttons_frame, text="LED ВЫКЛ", command=led_off, style='Custom.TButton', width=12)
off_btn.grid(column=1, row=0, padx=5, pady=5)

blue_btn = ttk.Button(buttons_frame, text="Blue LED", command=blue_led, style='Custom.TButton', width=12)
blue_btn.grid(column=2, row=0, padx=5, pady=5)

# Вторая строка кнопок
red_btn = ttk.Button(buttons_frame, text="Red LED", command=red_led, style='Custom.TButton', width=12)
red_btn.grid(column=0, row=1, padx=5, pady=5)

about_btn = ttk.Button(buttons_frame, text="Справка", command=about_message, style='Custom.TButton', width=12)
about_btn.grid(column=1, row=1, padx=5, pady=5)

quit_btn = ttk.Button(buttons_frame, text="Закрыть", command=win.destroy, style='Custom.TButton', width=12)
quit_btn.grid(column=2, row=1, padx=5, pady=5)

# Дополнительные функции
def toggle_theme():
    """Переключение между светлой и темной темами"""
    global bg_color, frame_bg, text_color, accent_color
    if bg_color == '#2b2b2b':
        bg_color = '#f0f0f0'
        frame_bg = '#ffffff'
        text_color = '#000000'
        accent_color = '#606060'
    else:
        bg_color = '#2b2b2b'
        frame_bg = '#3c3c3c'
        text_color = '#e0e0e0'
        accent_color = '#808080'
    
    win.configure(bg=bg_color)
    header_frame.configure(bg=bg_color)
    circle_frame.configure(bg=bg_color)
    title_label.configure(bg=bg_color, fg=accent_color)
    
    # Обновляем стили
    style.configure('Title.TLabel', background=bg_color, foreground=accent_color)
    style.configure('Custom.TLabel', background=frame_bg, foreground=text_color)
    style.configure('Custom.TButton', background=button_bg, foreground=text_color)

# Кнопка переключения темы
theme_btn = ttk.Button(buttons_frame, text="Тема", command=toggle_theme, style='Custom.TButton', width=12)
theme_btn.grid(column=0, row=2, columnspan=3, padx=5, pady=(10, 0))

# Настройка растяжимости
win.columnconfigure(0, weight=1)
win.rowconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

# Запускаем анимацию кружочков
animate_circles()

# Центрируем окно на экране
win.update_idletasks()
width = win.winfo_width()
height = win.winfo_height()
x = (win.winfo_screenwidth() // 2) - (width // 2)
y = (win.winfo_screenheight() // 2) - (height // 2)
win.geometry(f'{width}x{height}+{x}+{y}')

# Запускаем основное окно
win.mainloop()
