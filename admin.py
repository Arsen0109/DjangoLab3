from tkinter import *
from CRUD import car_crud, trademark_crud


def call_car_crud():
    car_crud_interface = Tk()
    car_crud.CarAdmin(car_crud_interface)
    car_crud_interface.mainloop()


def call_trademark_crud():
    trademark_crud_interface = Tk()
    trademark_crud.TrademarkAdmin(trademark_crud_interface)
    trademark_crud_interface.mainloop()


class AdminInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Admin")
        self.init_widgets()

    def init_widgets(self):
        car_interface_button = Button(self.master, text="Адмінка для автомобілів", command=call_car_crud,
                                      width=20, height=3)
        car_interface_button.grid(row=0, column=0)

        trademark_interface_button = Button(self.master, text="Адмінка для компаній", command=call_trademark_crud,
                                            width=20, height=3)
        trademark_interface_button.grid(row=0, column=1)


root = Tk()
admin_interface = AdminInterface(root)
root.mainloop()
