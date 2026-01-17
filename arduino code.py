import tkinter as tk
from tkinter import messagebox
#from pyfirmata import Arduino, PWM
#from time import sleep

#def blueLED():
    #delay = float(LEDtime.get())
    #brightness = float(LEDbright.get())
    #blueBtn.config(state = tk.DISABLED)
    #board.digital[3].write(brightness/100.0)
    #sleep(delay)
    #board.digital[3].write(0)
    #blueBtn.config(state = tk.ACTIVE)
#def redLED():
    #delay = float(LEDtime.get())

    #board.digital[5].write(0)
def aboutMsg():
    messagebox.showinfo("Это программное обеспечение," \
    " которому все равно на логику\nLED Контроллер Вер 1.0\nJanuary 2026")

#board = Arduino("COM3")

win = tk.Tk()
# инициализация окна
win.title("Dimmer LED")
win.minsize(270,190)

LEDtime = tk.Entry(win, bd=6, width=8)
LEDtime.grid(column=1, row=1)

tk.Label(win, text="LED ВКЛ Время (сек)").grid(column=2, row=1)

LEDbright = tk.Scale(win, bd=5, from_=0, to=100, orient=tk.HORIZONTAL)
LEDbright.grid(column=1, row=2)

tk.Label(win, text="Яркость LED")

blueBtn = tk.Button(win, bd=5, text="Blue LED",) #command-blueLED)
blueBtn.grid(column=1, row=3)
redBtn = tk.Button(win, bd=5, text="Red LED",) #command-redLED)
redBtn.grid(column=2, row=3)
aboutBtn = tk.Button(win, text="Справка",) #command-aboutMsg)
aboutBtn.grid(column=1, row=4)
quitBtn = tk.Button(win, text="Закрыть",) #command-win.quit)
quitBtn.grid(column=2, row=4)

label = tk.Label(win, text="Нажмите, чтобы вкл/выкл")
label.grid (column=2, row=1)

ONbtn = tk.Button(win, bd=4, text="LED ВКЛ",) # command=ledON)
ONbtn.grid(column=3, row=1)
OFFbtn = tk.Button(win, bd=4, text="LED ВЫКЛ",) # command=ledOFF)
OFFbtn.grid(column=3, row=2)
win = tk.Tk()
win.title("Red Button Example")
win.geometry("200x100")

# Создание метки с пояснением
label = tk.Label(win, text="Нажмите красную кнопку!")
label.pack(pady=10)

# Функция, выполняемая при нажатии на кнопку
def on_button_click():
    print("Красная кнопка нажата!")

# Создаем красную кнопку
red_button = tk.Button(
    win,
    text="Красный",
    bg="red",           # Цвет фона кнопки красный
    fg="white",          # Цвет текста белый
    font=("Arial", 14),
    width=10,
    height=2,
    command=on_button_click
)
red_button.pack(pady=10)

win.mainloop()