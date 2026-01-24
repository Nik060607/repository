import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import threading
import time

class ArduinoRedButton:
    """Современная красная кнопка с эффектами Arduino"""
    
    def __init__(self, parent, text="Красный!", command=None):
        self.parent = parent
        self.original_text = text
        self.command = command
        self.is_pressed = False
        self.is_connected = False
        self.led_state = False
        
        # Цвета для Arduino стиля
        self.colors = {
            'red_normal': '#ff0000',
            'red_pressed': '#cc0000',
            'red_hover': '#ff3333',
            'led_off': '#330000',
            'led_on': '#ff4444',
            'led_blink': '#ff8888',
            'arduino_bg': '#2b2b2b',
            'arduino_frame': '#3a3a3a',
            'arduino_metal': '#666666'
        }
        
        # Настройка шрифтов
        self.button_font = tkfont.Font(family='Courier New', size=12, weight='bold')
        self.status_font = tkfont.Font(family='Courier New', size=9)
        
        self._create_widgets()
        self._setup_bindings()
        self._start_connection_animation()
    
    def _create_widgets(self):
        """Создание виджетов кнопки Arduino"""
        # Основной фрейм стиля Arduino
        self.main_frame = tk.Frame(self.parent, bg=self.colors['arduino_bg'], bd=2, relief=tk.RAISED)
        
        # Верхняя панель (имитация металла)
        self.top_frame = tk.Frame(
            self.main_frame,
            bg=self.colors['arduino_metal'],
            height=5
        )
        self.top_frame.pack(fill=tk.X)
        
        # Фрейм для содержимого
        self.content_frame = tk.Frame(self.main_frame, bg=self.colors['arduino_frame'], padx=20, pady=15)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # LED индикатор подключения
        self.led_frame = tk.Frame(self.content_frame, bg=self.colors['arduino_frame'])
        self.led_frame.pack()
        
        self.led_canvas = tk.Canvas(
            self.led_frame,
            width=20,
            height=20,
            bg=self.colors['arduino_frame'],
            highlightthickness=0
        )
        self.led_canvas.pack(side=tk.LEFT, padx=(0, 10))
        
        self.led_id = self.led_canvas.create_oval(2, 2, 18, 18, fill=self.colors['led_off'])
        
        self.led_label = tk.Label(
            self.led_frame,
            text="DISCONNECTED",
            font=self.status_font,
            fg='#ff6666',
            bg=self.colors['arduino_frame']
        )
        self.led_label.pack(side=tk.LEFT)
        
        # Канвас для круглой кнопки
        self.canvas = tk.Canvas(
            self.content_frame,
            width=100,
            height=100,
            bg=self.colors['arduino_frame'],
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # Создание круглой кнопки с 3D эффектом
        self._create_3d_button()
        
        # Текст кнопки
        self.text_id = self.canvas.create_text(
            50, 50,
            text=self.original_text,
            fill='white',
            font=self.button_font,
            justify='center'
        )
        
        # Нижняя информационная панель
        self.info_frame = tk.Frame(self.content_frame, bg=self.colors['arduino_frame'])
        self.info_frame.pack()
        
        self.pin_label = tk.Label(
            self.info_frame,
            text="PIN: D13",
            font=self.status_font,
            fg='#888888',
            bg=self.colors['arduino_frame']
        )
        self.pin_label.pack(side=tk.LEFT, padx=5)
        
        self.voltage_label = tk.Label(
            self.info_frame,
            text="5V",
            font=self.status_font,
            fg='#888888',
            bg=self.colors['arduino_frame']
        )
        self.voltage_label.pack(side=tk.LEFT, padx=5)
        
        # Статус нажатия
        self.status_label = tk.Label(
            self.content_frame,
            text="Status: READY",
            font=self.status_font,
            fg='#88ff88',
            bg=self.colors['arduino_frame']
        )
        self.status_label.pack(pady=(10, 0))
    
    def _create_3d_button(self):
        """Создание кнопки с 3D эффектом"""
        # Внешнее кольцо (металлическое)
        self.canvas.create_oval(5, 5, 95, 95, 
                               fill=self.colors['arduino_metal'], 
                               outline='#444444', 
                               width=2)
        
        # Основная кнопка с градиентом
        for i in range(30, 70):
            color_intensity = int(255 * (1 - abs(i - 50) / 20))
            color = f'#{color_intensity:02x}0000'
            self.canvas.create_oval(i-20, i-20, 100-(i-20), 100-(i-20), 
                                   fill=color, outline='')
        
        # Верхняя часть кнопки (выпуклая)
        self.button_top_id = self.canvas.create_oval(25, 25, 75, 75, 
                                                    fill=self.colors['red_normal'],
                                                    outline='#aa0000',
                                                    width=2)
        
        # Эффект блика
        self.canvas.create_oval(30, 30, 45, 45, fill='#ff6666', outline='')
        
        # Тень под кнопкой
        self.canvas.create_oval(28, 28, 78, 78, fill='#550000', outline='')
    
    def _setup_bindings(self):
        """Настройка обработчиков событий"""
        self.canvas.bind("<Enter>", self._on_enter)
        self.canvas.bind("<Leave>", self._on_leave)
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        
        # Изменение курсора при наведении
        self.canvas.bind("<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.bind("<Leave>", lambda e: self.canvas.config(cursor=""))
    
    def _on_enter(self, event):
        """Обработка наведения курсора"""
        if not self.is_pressed:
            self.canvas.itemconfig(self.button_top_id, fill=self.colors['red_hover'])
            self.status_label.config(text="Status: HOVER")
    
    def _on_leave(self, event):
        """Обработка ухода курсора"""
        if not self.is_pressed:
            self.canvas.itemconfig(self.button_top_id, fill=self.colors['red_normal'])
            self.status_label.config(text="Status: READY")
    
    def _on_click(self, event):
        """Обработка нажатия кнопки"""
        self.is_pressed = True
        
        # Анимация нажатия
        self.canvas.move(self.button_top_id, 2, 2)
        self.canvas.move(self.text_id, 2, 2)
        
        # Изменение цвета
        self.canvas.itemconfig(self.button_top_id, fill=self.colors['red_pressed'])
        
        # Обновление статуса
        self.status_label.config(text="Status: PRESSED", fg='#ffff88')
        
        # Симуляция отправки сигнала на Arduino
        self._simulate_arduino_signal()
        
        # Визуальная обратная связь
        self._create_press_effect()
        
        # Выполнение команды пользователя
        if self.command:
            threading.Thread(target=self._execute_command, daemon=True).start()
    
    def _on_release(self, event):
        """Обработка отпускания кнопки"""
        self.is_pressed = False
        
        # Возврат в исходное положение
        self.canvas.move(self.button_top_id, -2, -2)
        self.canvas.move(self.text_id, -2, -2)
        
        # Восстановление цвета
        if self.canvas.winfo_pointerxy()[0] - self.canvas.winfo_rootx() in range(100):
            self.canvas.itemconfig(self.button_top_id, fill=self.colors['red_hover'])
            self.status_label.config(text="Status: HOVER", fg='#88ff88')
        else:
            self.canvas.itemconfig(self.button_top_id, fill=self.colors['red_normal'])
            self.status_label.config(text="Status: READY", fg='#88ff88')
    
    def _create_press_effect(self):
        """Создание эффекта нажатия (рябь)"""
        for i in range(5, 50, 5):
            ripple_id = self.canvas.create_oval(
                50-i, 50-i, 50+i, 50+i,
                outline='#ff0000',
                width=1
            )
            self.parent.after(i*10, lambda rid=ripple_id: self.canvas.delete(rid))
    
    def _simulate_arduino_signal(self):
        """Симуляция отправки сигнала на Arduino"""
        def blink_led():
            for _ in range(3):
                self.canvas.itemconfig(self.led_id, fill=self.colors['led_on'])
                self.parent.update()
                time.sleep(0.1)
                self.canvas.itemconfig(self.led_id, fill=self.colors['led_off'])
                self.parent.update()
                time.sleep(0.1)
            
            if self.is_connected:
                self.canvas.itemconfig(self.led_id, fill=self.colors['led_blink'])
        
        threading.Thread(target=blink_led, daemon=True).start()
    
    def _execute_command(self):
        """Выполнение пользовательской команды"""
        time.sleep(0.1)  # Задержка для реалистичности
        self.command()
    
    def _start_connection_animation(self):
        """Анимация подключения к Arduino"""
        def connect_sequence():
            # Поиск устройства
            self.led_label.config(text="SEARCHING...", fg='#ffff88')
            
            for i in range(5):
                self.canvas.itemconfig(self.led_id, fill=self.colors['led_blink'])
                self.parent.update()
                time.sleep(0.3)
                self.canvas.itemconfig(self.led_id, fill=self.colors['led_off'])
                self.parent.update()
                time.sleep(0.3)
            
            # Подключение
            self.led_label.config(text="CONNECTING...", fg='#ffff88')
            time.sleep(1)
            
            # Подключено
            self.is_connected = True
            self.led_label.config(text="CONNECTED", fg='#88ff88')
            self.canvas.itemconfig(self.led_id, fill=self.colors['led_on'])
            
            # Мерцание LED
            self._start_led_animation()
        
        threading.Thread(target=connect_sequence, daemon=True).start()
    
    def _start_led_animation(self):
        """Анимация мерцания LED"""
        def animate():
            while self.is_connected:
                current_color = self.canvas.itemcget(self.led_id, "fill")
                if current_color == self.colors['led_on']:
                    self.canvas.itemconfig(self.led_id, fill=self.colors['led_blink'])
                else:
                    self.canvas.itemconfig(self.led_id, fill=self.colors['led_on'])
                time.sleep(1)
        
        threading.Thread(target=animate, daemon=True).start()
    
    def connect(self):
        """Публичный метод для подключения"""
        self.is_connected = True
        self.led_label.config(text="CONNECTED", fg='#88ff88')
        self.canvas.itemconfig(self.led_id, fill=self.colors['led_on'])
        self._start_led_animation()
    
    def disconnect(self):
        """Публичный метод для отключения"""
        self.is_connected = False
        self.led_label.config(text="DISCONNECTED", fg='#ff6666')
        self.canvas.itemconfig(self.led_id, fill=self.colors['led_off'])
    
    def pack(self, **kwargs):
        """Упаковка кнопки"""
        self.main_frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Размещение кнопки в сетке"""
        self.main_frame.grid(**kwargs)

# Основная программа
if __name__ == "__main__":
    # Инициализация окна
    win = tk.Tk()
    win.title("Arduino Red Button Controller")
    win.geometry("400x500")
    win.configure(bg='#1a1a1a')
    
    # Загрузка шрифта для заголовка
    title_font = tkfont.Font(family='Courier New', size=16, weight='bold')
    
    # Заголовок
    title_frame = tk.Frame(win, bg='#1a1a1a')
    title_frame.pack(fill=tk.X, pady=20)
    
    title_label = tk.Label(
        title_frame,
        text="⚡ ARDUINO RED BUTTON ⚡",
        font=title_font,
        fg='#ff4444',
        bg='#1a1a1a'
    )
    title_label.pack()
    
    subtitle_label = tk.Label(
        title_frame,
        text="Press the emergency stop button",
        font=('Courier New', 10),
        fg='#888888',
        bg='#1a1a1a'
    )
    subtitle_label.pack(pady=(5, 0))
    
    # Центрирующий фрейм
    center_frame = tk.Frame(win, bg='#1a1a1a')
    center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # Логика кнопки
    def on_button_click():
        print("Красная кнопка Arduino нажата!")
        print("Отправка сигнала на PIN D13...")
        print("Напряжение: 5V")
        messagebox.showwarning("EMERGENCY STOP", 
                             "⚠️ КРАСНАЯ КНОПКА НАЖАТА!\n\n"
                             "Аварийная остановка активирована!\n"
                             "Отправлен сигнал на Arduino UNO\n"
                             "PIN: D13 | Напряжение: 5V")
    
    # Создание красной кнопки Arduino
    arduino_button = ArduinoRedButton(
        center_frame,
        text="STOP!",
        command=on_button_click
    )
    arduino_button.pack()
    
    # Панель управления
    control_frame = tk.Frame(win, bg='#2a2a2a', bd=1, relief=tk.RIDGE)
    control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)
    
    # Кнопки управления
    def connect_arduino():
        arduino_button.connect()
        messagebox.showinfo("Подключение", "Arduino подключен успешно!")
    
    def disconnect_arduino():
        arduino_button.disconnect()
        messagebox.showinfo("Отключение", "Arduino отключен")
    
    connect_btn = ttk.Button(
        control_frame,
        text="Подключить Arduino",
        command=connect_arduino,
        style="Arduino.TButton"
    )
    connect_btn.pack(side=tk.LEFT, padx=10, pady=10)
    
    disconnect_btn = ttk.Button(
        control_frame,
        text="Отключить Arduino",
        command=disconnect_arduino,
        style="Arduino.TButton"
    )
    disconnect_btn.pack(side=tk.LEFT, padx=10, pady=10)
    
    # Стиль для кнопок управления
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Arduino.TButton",
                   background='#444444',
                   foreground='white',
                   font=('Courier New', 10),
                   borderwidth=1,
                   relief=tk.RAISED)
    style.map("Arduino.TButton",
             background=[('active', '#555555')])
    
    # Центрирование окна
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f'{width}x{height}+{x}+{y}')
    
    # Запускаем основное окно
    win.mainloop()
