import tkinter as tk
from tkinter import ttk
import threading
import time

# Имитируем управление двигателем (замена реальной интеграции)
class StepperMotorSimulator:
    def __init__(self):
        self.is_running = False
        self.speed = 0
        self.direction = 'CW'  # CW (Clockwise) or CCW (Counter-Clockwise)
    
    def start(self):
        if not self.is_running:
            print("Двигатель запущен.")
            self.is_running = True
        
    def stop(self):
        if self.is_running:
            print("Двигатель остановлен.")
            self.is_running = False
            
    def set_speed(self, speed_value):
        self.speed = speed_value
        print(f"Скорость установлена на {speed_value}.")
        
    def change_direction(self, direction):
        self.direction = direction
        print(f"Направление установлено на {'По часовой стрелке' if direction == 'CW' else 'Против часовой стрелки'}.")

# Класс главного окна приложения
class MotorControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Управление шаговым двигателем')
        self.geometry('400x300')
        
        # Создаем объект имитатора двигателя
        self.motor_simulator = StepperMotorSimulator()
        
        # Элементы интерфейса
        frame_buttons = tk.Frame(self)
        frame_buttons.pack(pady=10)
        
        btn_start = tk.Button(frame_buttons, text="Старт", command=self.start_motor)
        btn_stop = tk.Button(frame_buttons, text="Стоп", command=self.stop_motor)
        
        btn_start.grid(row=0, column=0, padx=(0, 10))
        btn_stop.grid(row=0, column=1)
        
        label_speed = tk.Label(self, text='Скорость:')
        label_speed.pack(pady=5)
        
        slider_speed = ttk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=200, command=lambda value: self.set_speed(float(value)))
        slider_speed.pack(pady=5)
        
        radio_frame = tk.Frame(self)
        radio_frame.pack(pady=10)
        
        var_radio = tk.StringVar(value='CW')  # По умолчанию вращаем по часовой стрелке
        
        radio_cw = tk.Radiobutton(radio_frame, text='По часовой', variable=var_radio, value='CW', command=lambda: self.change_direction(var_radio.get()))
        radio_ccw = tk.Radiobutton(radio_frame, text='Против часовой', variable=var_radio, value='CCW', command=lambda: self.change_direction(var_radio.get()))
        
        radio_cw.pack(side=tk.LEFT, padx=10)
        radio_ccw.pack(side=tk.RIGHT, padx=10)
        
        # Простое уведомление для анимации
        self.label_status = tk.Label(self, text='', font=('Arial', 12, 'bold'))
        self.label_status.pack(pady=10)
        
        # Функция для обновления статуса
        self.update_status_thread = None
        self.update_status()
    
    def update_status(self):
        """Обновляем статус двигателя"""
        if self.motor_simulator.is_running:
            self.label_status.config(text=f"Двигатель включен\nСкорость: {self.motor_simulator.speed}\nНаправление: {self.motor_simulator.direction}")
        else:
            self.label_status.config(text="Двигатель выключен")
        self.after(1000, self.update_status)
    
    def start_motor(self):
        self.motor_simulator.start()
    
    def stop_motor(self):
        self.motor_simulator.stop()
    
    def set_speed(self, speed_value):
        self.motor_simulator.set_speed(speed_value)
    
    def change_direction(self, direction):
        self.motor_simulator.change_direction(direction)

if __name__ == "__main__":
    app = MotorControlApp()
    app.mainloop()
