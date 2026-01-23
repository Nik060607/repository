from tkinter import *
from tkinter.ttk import Style

class App(Tk):
    def __init__(self):
        super().__init__()
        
        # Новый стиль
        s = Style()
        s.theme_use('clam')
        
        # Заголовок окна
        self.title("Форма регистрации")
        
        # Рамка для формы
        frm = Frame(self)
        frm.pack(expand=True, fill=BOTH)
        
        # Метка для поля Имя
        lbl_name = Label(frm, text="Имя:", anchor=E)
        lbl_name.grid(row=0, column=0, sticky=EW)
        
        # Поле ввода имени
        entry_name = Entry(frm)
        entry_name.grid(row=0, column=1, sticky=EW)
        
        # Метка для поля Возраст
        lbl_age = Label(frm, text="Возраст:", anchor=E)
        lbl_age.grid(row=1, column=0, sticky=EW)
        
        # Поле ввода возраста
        entry_age = Spinbox(frm, from_=0, to=100)
        entry_age.grid(row=1, column=1, sticky=EW)
        
        # Кнопка отправки формы
        submit_btn = Button(frm, text="Отправить", bg="#00ff00", fg="white")
        submit_btn.grid(row=2, columnspan=2, sticky=EW)

if __name__ == "__main__":
    app = App()
    app.mainloop()