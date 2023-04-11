import tkinter as tk
import tkinter.messagebox as messagebox
from pymongo import MongoClient
from .car_crud import CarDB
from bson.objectid import ObjectId


def trademark_to_str(trademark):
    return f"{trademark['_id']} {trademark['trademark_name']}"


def car_to_str(car):
    return f"{car['make']} {car['model']} {car['year']} {car['price']}"


class TrademarkDB:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.cartrademarks
        self.trademark_collection = self.db.trademark_collection

    # Метод створення нового елементу в колекції "trademark_collection"
    def create_trademark(self, trademark_data):
        trademark_id = self.trademark_collection.insert_one(trademark_data).inserted_id
        return self.get_trademark_by_id(trademark_id)

    # Метод отримання всіх елементів з колекції "trademark_collection"
    def get_all_trademarks(self):
        trademarks = []
        for trademark in self.trademark_collection.find():
            trademark['_id'] = str(trademark['_id'])
            trademarks.append(trademark)
        return trademarks

    # Метод отримання елемента з колекції "trademark_collection" за його id
    def get_trademark_by_id(self, trademark_id):
        trademark = self.trademark_collection.find_one({'_id': ObjectId(trademark_id)})
        if trademark:
            trademark['_id'] = str(trademark['_id'])
            return trademark
        else:
            return None

    # Метод оновлення елемента в колекції "trademark_collection" за його id
    def update_trademark(self, trademark_id, trademark_data):
        self.trademark_collection.update_one({'_id': ObjectId(trademark_id)}, {'$set': trademark_data})
        return self.get_trademark_by_id(trademark_id)

    # Метод для видалення елемента з колекції
    def delete_trademark(self, trademark_id):
        deleted_trademark = self.get_trademark_by_id(trademark_id)
        self.trademark_collection.delete_one({"_id": ObjectId(trademark_id)})
        return deleted_trademark


class TrademarkAdmin:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Admin")
        self.trademark_listbox = tk.Listbox(self.master, width=40, height=20)
        self.car_id_listbox = tk.Listbox(self.master)
        self.car_id_entry = tk.Entry(self.master, width=20)
        self.trademark_name_entry = tk.Entry(self.master)
        self.trademark_id_entry = tk.Entry(self.master, width=20)
        self.info_label = tk.Label(self.master, font="Arial 10")
        self.init_widgets()
        self.clear_car_listbox()
        self.fill_trademark_listbox()

    def init_widgets(self):
        tk.Label(self.master, text="Створити компанію:", font="Arial 10 bold").grid(row=0, column=0)
        make_label = tk.Label(self.master, text="Назва компанії:")
        make_label.grid(row=1, column=0, sticky=tk.E)
        self.trademark_name_entry.grid(row=1, column=1)

        tk.Label(self.master, text="Отримати компанію за id", font="Arial 10 bold").grid(row=2, column=0)
        tk.Label(self.master, text="ID компанії:").grid(row=3, column=0, sticky=tk.E)
        self.trademark_id_entry.grid(row=3, column=1)

        tk.Label(self.master, text="Редагувати список car_id:", font="Arial 10 bold").grid(row=4, column=0)
        tk.Label(self.master, text="car_id:", font="Arial 10").grid(row=5, column=0, sticky=tk.E)
        self.car_id_entry.grid(row=5, column=1)

        self.car_id_listbox.grid(row=8, column=2)
        self.car_id_listbox.bind("<<ListboxSelect>>", self.on_select_car)

        add_car_id_button = tk.Button(self.master, text="Додати id для авто", command=self.add_car_id)
        add_car_id_button.grid(row=7, column=1)

        delete_car_id_button = tk.Button(self.master, text="Видалити id для авто", command=self.delete_car_id)
        delete_car_id_button.grid(row=7, column=2)

        self.trademark_listbox.grid(row=8, column=0, columnspan=2)
        self.trademark_listbox.bind("<<ListboxSelect>>", self.on_select_trademark)

        get_button = tk.Button(self.master, text="Отримати компанію", command=self.show_trademark_by_id)
        get_button.grid(row=3, column=2)

        add_button = tk.Button(self.master, text="Додати компанію", command=self.add_trademark)
        add_button.grid(row=11, column=0)

        update_button = tk.Button(self.master, text="Оновити компанію", command=self.update_trademark)
        update_button.grid(row=11, column=1)

        delete_button = tk.Button(self.master, text="Видалити компанію", command=self.delete_trademark)
        delete_button.grid(row=11, column=2)

        clear_button = tk.Button(self.master, text="Очистити форми", command=self.clear_form)
        clear_button.grid(row=11, column=3)

        self.info_label.grid(row=10, column=1)

    def fill_car_listbox(self, trademark):
        self.car_id_listbox.delete(0, tk.END)
        for car_id in trademark['cars']:
            self.car_id_listbox.insert(0, car_to_str(CarDB().get_car_by_id(car_id)))

    def fill_trademark_listbox(self):
        self.trademark_listbox.delete(0, tk.END)
        for trademark in TrademarkDB().get_all_trademarks():
            self.trademark_listbox.insert(0, trademark_to_str(trademark))

    def add_car_id(self):
        car_id = self.car_id_entry.get()
        if car_id:
            self.car_id_listbox.insert(0, car_id)
        else:
            messagebox.showerror("Error", "Поле car_id є обовязковим")

    def delete_car_id(self):
        car_id = self.car_id_entry.get()
        if car_id:
            index = self.car_id_listbox.get(0, tk.END).index(str(car_id))
            self.car_id_listbox.delete(index)
        else:
            messagebox.showerror("Error", "Поле car_id є обовязковим")

    def show_trademark_by_id(self):
        trademark_id = self.trademark_id_entry.get()
        if trademark_id:
            trademark = TrademarkDB().get_trademark_by_id(trademark_id)
            self.trademark_name_entry.delete(0, tk.END)
            self.trademark_name_entry.insert(0, trademark.trademark_name or '')
            self.fill_car_listbox(trademark)

        else:
            messagebox.showerror("Error", "Поле ID є обовязковим.")

    def add_trademark(self):
        trademark_name = self.trademark_name_entry.get()
        if trademark_name:
            self.clear_form()
            created_trademark_id = TrademarkDB().create_trademark({'trademark_name': trademark_name, 'cars': []})
            print('Created trademark:\n', created_trademark_id)
            self.info_label["text"] = "Компанія успішно додана до БД"
            self.info_label["bg"] = "Green"

        else:
            messagebox.showerror("Error", "Як мінімум поле назви є обовязковим")
        self.fill_trademark_listbox()

    def update_trademark(self):
        trademark_id = self.trademark_id_entry.get()
        if trademark_id:
            trademark_name = self.trademark_name_entry.get()
            if trademark_name:
                index = self.trademark_listbox.get(0, tk.END)\
                    .index(trademark_to_str(TrademarkDB().get_trademark_by_id(trademark_id)))
                self.trademark_listbox.delete(index)
                print('Оновлена компанія:\n',
                      TrademarkDB().update_trademark(trademark_id,
                                         {'trademark_name': trademark_name,
                                          'cars': [ObjectId(car_id) for car_id in self.car_id_listbox.get(0, tk.END)]
                                          }
                                         ))
                self.trademark_listbox.insert(0, trademark_to_str(TrademarkDB().get_trademark_by_id(trademark_id)))
                self.clear_form()
                self.info_label["text"] = "Компанія успішно оновлена"
                self.info_label["bg"] = "Green"
            else:
                messagebox.showerror("Error", "Як мінімум поле назви є обовязковим")
        else:
            messagebox.showerror("Error", "Поле ID є обовязковим.")

    def delete_trademark(self):
        trademark_id = self.trademark_id_entry.get()
        if trademark_id:
            index = self.trademark_listbox.get(0, tk.END)\
                .index(trademark_to_str(TrademarkDB().get_trademark_by_id(trademark_id)))
            self.trademark_listbox.delete(index)
            print('Видалена компанія:\n', TrademarkDB().delete_trademark(trademark_id))
            self.clear_form()
            self.info_label["text"] = "Компанія успішно видалена з БД"
            self.info_label["bg"] = "Green"
        else:
            messagebox.showerror("Error", "Поле ID є обовязковим..")

    def clear_form(self):
        self.trademark_name_entry.delete(0, tk.END)
        self.clear_car_listbox()
        self.trademark_id_entry.delete(0, tk.END)
        self.car_id_entry.delete(0, tk.END)

    def clear_car_listbox(self):
        self.car_id_listbox.delete(0, tk.END)

    def on_select_trademark(self, event):
        index = self.trademark_listbox.curselection()
        if index:
            trademark = self.trademark_listbox.get(index)
            trademark_id, trademark_name = self.parse_trademark(trademark)
            self.trademark_name_entry.delete(0, tk.END)
            self.trademark_name_entry.insert(0, trademark_name)
            self.trademark_id_entry.delete(0, tk.END)
            self.trademark_id_entry.insert(0, trademark_id)
            self.car_id_listbox.delete(0, tk.END)
            for car_id in TrademarkDB().get_trademark_by_id(trademark_id)['cars']:
                print(car_id)
                self.car_id_listbox.insert(0, str(car_id))

    def on_select_car(self, event):
        index = self.car_id_listbox.curselection()
        if index:
            car_id = self.car_id_listbox.get(index)
            self.car_id_entry.insert(0, car_id)

    def parse_trademark(self, car):
        trademark_id, trademark_name = car.split(" ")
        return trademark_id, trademark_name

