import tkinter as tk
import tkinter.messagebox as messagebox
from pymongo import MongoClient
from bson.objectid import ObjectId


def car_to_str(car):
    return f"{car['_id']} {car['make']} {car['model']} {car['year']} {car['price']}"


class CarDB:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.cartrademarks
        self.car_collection = self.db.car_collection

    # Метод створення нового елементу в колекції "car_collection"
    def create_car(self, car_data):
        car_id = self.car_collection.insert_one(car_data).inserted_id
        return self.get_car_by_id(car_id)

    # Метод отримання всіх елементів з колекції "car_collection"
    def get_all_cars(self):
        cars = []
        for car in self.car_collection.find():
            car['_id'] = str(car['_id'])
            cars.append(car)
        return cars

    # Метод отримання елемента з колекції "car_collection" за його id
    def get_car_by_id(self, car_id):
        car = self.car_collection.find_one({'_id': ObjectId(car_id)})
        if car:
            car['_id'] = str(car['_id'])
            return car
        else:
            return None

    # Метод оновлення елемента в колекції "car_collection" за його id
    def update_car(self, car_id, car_data):
        self.car_collection.update_one({'_id': ObjectId(car_id)}, {'$set': car_data})
        return self.get_car_by_id(car_id)

    # Метод видалення елемента з колекції "car_collection" за його id
    def delete_car(self, car_id):
        deleted_car = self.get_car_by_id(car_id)
        self.car_collection.delete_one({'_id': ObjectId(car_id)})
        return deleted_car


class CarAdmin:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Admin")
        self.car_listbox = tk.Listbox(self.master, width=50, height=20)
        self.year_entry = tk.Entry(self.master)
        self.model_entry = tk.Entry(self.master)
        self.make_entry = tk.Entry(self.master)
        self.price_entry = tk.Entry(self.master)
        self.car_id_entry = tk.Entry(self.master, width=15)
        self.info_label = tk.Label(self.master, font="Arial 10")
        self.init_widgets()
        self.fill_car_listbox()

    def init_widgets(self):
        tk.Label(self.master, text="Створити авто:", font="Arial 10 bold").grid(row=0, column=0)
        make_label = tk.Label(self.master, text="Марка:")
        make_label.grid(row=1, column=0)
        self.make_entry.grid(row=1, column=1)

        model_label = tk.Label(self.master, text="Модель:")
        model_label.grid(row=2, column=0)
        self.model_entry.grid(row=2, column=1)

        year_label = tk.Label(self.master, text="Рік:")
        year_label.grid(row=3, column=0)
        self.year_entry.grid(row=3, column=1)

        price_label = tk.Label(self.master, text="Ціна:")
        price_label.grid(row=4, column=0)
        self.price_entry.grid(row=4, column=1)

        tk.Label(self.master, text="Отримати авто за id", font="Arial 10 bold").grid(row=6, column=0)
        tk.Label(self.master, text="ID авто:").grid(row=7, column=0)
        self.car_id_entry.grid(row=7, column=1)

        self.car_listbox.grid(row=8, column=0, columnspan=2)
        self.car_listbox.bind("<<ListboxSelect>>", self.on_select_car)

        get_button = tk.Button(self.master, text="Отримати авто", command=self.show_car_by_id)
        get_button.grid(row=7, column=2)

        add_button = tk.Button(self.master, text="Додати авто", command=self.add_car)
        add_button.grid(row=11, column=0)

        update_button = tk.Button(self.master, text="Оновити авто", command=self.update_car)
        update_button.grid(row=11, column=1)

        delete_button = tk.Button(self.master, text="Видалити авто", command=self.delete_car)
        delete_button.grid(row=11, column=2)

        clear_button = tk.Button(self.master, text="Очистити форми", command=self.clear_form)
        clear_button.grid(row=11, column=3)

        self.info_label.grid(row=10, column=1)

    def fill_car_listbox(self):
        self.car_listbox.delete(0, tk.END)
        for car in CarDB().get_all_cars():
            self.car_listbox.insert(0, car_to_str(car))

    def show_car_by_id(self):
        car_id = self.car_id_entry.get()
        if car_id:
            car = CarDB().get_car_by_id(car_id)
            self.make_entry.delete(0, tk.END)
            self.make_entry.insert(0, car.make or '')
            self.model_entry.delete(0, tk.END)
            self.model_entry.insert(0, car.model_id or '')
            self.year_entry.delete(0, tk.END)
            self.year_entry.insert(0, car.year or '')
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, car.price or '')

        else:
            messagebox.showerror("Error", "Поле ID є обовязковим.")

    def add_car(self):
        make = self.make_entry.get()
        model = self.model_entry.get()
        year = self.year_entry.get()
        price = self.price_entry.get()
        if make and year and price and model:
            self.clear_form()
            print('Created car:\n', CarDB().create_car({'make': make, 'model': model, 'year': year, 'price': price}))
            self.info_label["text"] = "Авто успішно додане до БД"
            self.info_label["bg"] = "Green"

        else:
            messagebox.showerror("Error", "Усі поля є обовязковими")
        self.fill_car_listbox()

    def update_car(self):
        car_id = self.car_id_entry.get()
        if car_id:
            make = self.make_entry.get()
            model = self.model_entry.get()
            year = self.year_entry.get()
            price = self.price_entry.get()
            if make and price and year and model:
                index = self.car_listbox.get(0, tk.END).index(car_to_str(CarDB().get_car_by_id(car_id)))
                self.car_listbox.delete(index)
                print('Updated car:\n', CarDB().update_car(car_id, {'make': make, 'model': model, 'year': year, 'price': price}))
                self.car_listbox.insert(0, car_to_str(CarDB().get_car_by_id(car_id)))
                self.clear_form()
                self.info_label["text"] = "Авто успішно оновлене"
                self.info_label["bg"] = "Green"
            else:
                messagebox.showerror("Error", "Як мінімум поля марки року та ціни є обовязковими")
        else:
            messagebox.showerror("Error", "Поле ID є обовязковим.")

    def delete_car(self):
        car_id = self.car_id_entry.get()
        if car_id:
            index = self.car_listbox.get(0, tk.END).index(str(car_to_str(CarDB().get_car_by_id(car_id))))
            self.car_listbox.delete(index)
            print('Deleted car:\n', CarDB().delete_car(car_id))
            self.clear_form()
            self.info_label["text"] = "Авто успішно видалене з БД"
            self.info_label["bg"] = "Green"
        else:
            messagebox.showerror("Error", "Поле ID є обовязковим..")

    def clear_form(self):
        self.make_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.car_id_entry.delete(0, tk.END)

    def on_select_car(self, event):
        index = self.car_listbox.curselection()
        if index:
            car = self.car_listbox.get(index)
            car_id, make, model, year, price = self.parse_car(car)
            self.make_entry.delete(0, tk.END)
            self.make_entry.insert(0, make)
            self.model_entry.delete(0, tk.END)
            self.model_entry.insert(0, model)
            self.year_entry.delete(0, tk.END)
            self.year_entry.insert(0, year)
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, price)
            self.car_id_entry.delete(0, tk.END)
            self.car_id_entry.insert(0, car_id)

    def parse_car(self, car):
        car_id, make, model, year, price = car.split(" ")
        return car_id, make, model, year, price
