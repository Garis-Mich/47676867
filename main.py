import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.records = []

        # Интерфейс
        self.create_widgets()
        self.load_records()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Дата (YYYY-MM-DD):").grid(row=0, column=0)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Температура:").grid(row=1, column=0)
        self.temp_entry = tk.Entry(self.root)
        self.temp_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Описание:").grid(row=2, column=0)
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.grid(row=2, column=1)

        self.rain_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Осадки", variable=self.rain_var).grid(row=3, column=0, columnspan=2)

        # Кнопки
        tk.Button(self.root, text="Добавить запись", command=self.add_record).grid(row=4, column=0)
        tk.Button(self.root, text="Сохранить", command=self.save_records).grid(row=4, column=1)
        tk.Button(self.root, text="Загрузить", command=self.load_records).grid(row=5, column=0)

        # Фильтры
        tk.Label(self.root, text="Фильтр по дате:").grid(row=6, column=0)
        self.filter_date = tk.Entry(self.root)
        self.filter_date.grid(row=6, column=1)
        tk.Button(self.root, text="Фильтровать", command=self.filter_by_date).grid(row=7, column=0)

        tk.Label(self.root, text="Фильтр по температуре >").grid(row=8, column=0)
        self.filter_temp = tk.Entry(self.root)
        self.filter_temp.grid(row=8, column=1)
        tk.Button(self.root, text="Фильтровать", command=self.filter_by_temp).grid(row=9, column=0)

        # Таблица записей
        self.tree = ttk.Treeview(self.root, columns=("date", "temp", "desc", "rain"), show='headings')
        self.tree.heading("date", text="Дата")
        self.tree.heading("temp", text="Температура")
        self.tree.heading("desc", text="Описание")
        self.tree.heading("rain", text="Осадки")
        self.tree.grid(row=10, column=0, columnspan=2)

    def add_record(self):
        date = self.date_entry.get()
        temp = self.temp_entry.get()
        desc = self.desc_entry.get()
        rain = self.rain_var.get()

        # Валидация
        try:
            datetime.strptime(date, "%Y-%m-%d")
            temp = float(temp)
            if not desc:
                raise ValueError("Описание не может быть пустым")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            return

        record = {"date": date, "temp": temp, "desc": desc, "rain": rain}
        self.records.append(record)
        self.update_tree()

    def update_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for rec in self.records:
            self.tree.insert("", "end", values=(rec["date"], rec["temp"], rec["desc"], "Да" if rec["rain"] else "Нет"))

    def filter_by_date(self):
        date = self.filter_date.get()
        try:
            datetime.strptime(date, "%Y-%m-%d")
            filtered = [r for r in self.records if r["date"] == date]
            self.update_tree(filtered)
        except:
            messagebox.showerror("Ошибка", "Неверный формат даты")

    def filter_by_temp(self):
        try:
            temp = float(self.filter_temp.get())
            filtered = [r for r in self.records if r["temp"] > temp]
            self.update_tree(filtered)
        except:
            messagebox.showerror("Ошибка", "Неверный формат температуры")

    def update_tree(self, records=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for rec in records or self.records:
            self.tree.insert("", "end", values=(rec["date"], rec["temp"], rec["desc"], "Да" if rec["rain"] else "Нет"))

    def save_records(self):
        with open("weather_diary.json", "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)

    def load_records(self):
        try:
            with open("weather_diary.json", "r", encoding="utf-8") as f:
                self.records = json.load(f)
                self.update_tree()
                return True
        except FileNotFoundError:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    root.mainloop()