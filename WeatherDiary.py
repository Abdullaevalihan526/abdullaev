import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.entries = []
        
        # Поля ввода
        tk.Label(root, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Температура (°C):").grid(row=1, column=0, padx=5, pady=5)
        self.temp_entry = tk.Entry(root)
        self.temp_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Описание погоды:").grid(row=2, column=0, padx=5, pady=5)
        self.desc_entry = tk.Entry(root)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Осадки:").grid(row=3, column=0, padx=5, pady=5)
        self.precip_var = tk.BooleanVar()
        tk.Checkbutton(root, variable=self.precip_var).grid(row=3, column=1, sticky="w")

        # Кнопка добавления
        tk.Button(root, text="Добавить запись", command=self.add_entry).grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица для отображения записей
        self.tree = ttk.Treeview(root, columns=("Date", "Temp", "Desc", "Precip"), show="headings")
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Temp", text="Температура")
        self.tree.heading("Desc", text="Описание")
        self.tree.heading("Precip", text="Осадки")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Фильтры
        tk.Label(root, text="Фильтр по дате:").grid(row=6, column=0, padx=5, pady=5)
        self.filter_date_entry = tk.Entry(root)
        self.filter_date_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(root, text="Фильтр по температуре (>):").grid(row=7, column=0, padx=5, pady=5)
        self.filter_temp_entry = tk.Entry(root)
        self.filter_temp_entry.grid(row=7, column=1, padx=5, pady=5)

        tk.Button(root, text="Применить фильтры", command=self.apply_filters).grid(row=8, column=0, columnspan=2, pady=5)

        # Кнопки сохранения/загрузки
        tk.Button(root, text="Сохранить в JSON", command=self.save_to_json).grid(row=9, column=0, pady=5)
        tk.Button(root, text="Загрузить из JSON", command=self.load_from_json).grid(row=9, column=1, pady=5)

    def add_entry(self):
        date_str = self.date_entry.get()
        temp_str = self.temp_entry.get()
        desc = self.desc_entry.get()
        precip = self.precip_var.get()

        # Проверка корректности
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте YYYY-MM-DD.")
            return

        try:
            temp = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом.")
            return

        if not desc:
            messagebox.showerror("Ошибка", "Описание не может быть пустым.")
            return

        # Добавление записи
        entry = {
            "date": date_str,
            "temperature": temp,
            "description": desc,
            "precipitation": "да" if precip else "нет"
        }
        self.entries.append(entry)
        self.update_table()

        # Очистка полей
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in self.entries:
            self.tree.insert("", "end", values=(
                entry["date"],
                entry["temperature"],
                entry["description"],
                entry["precipitation"]
            ))

    def apply_filters(self):
        filtered = self.entries

        # Фильтр по дате
        filter_date = self.filter_date_entry.get()
        if filter_date:
            filtered = [e for e in filtered if e["date"] == filter_date]

        # Фильтр по температуре
        filter_temp = self.filter_temp_entry.get()
        if filter_temp:
            try:
                temp_threshold = float(filter_temp)
                filtered = [e for e in filtered if e["temperature"] > temp_threshold]
            except ValueError:
                messagebox.showerror("Ошибка", "Температура для фильтра должна быть числом.")
                return

        # Обновление таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry in filtered:
            self.tree.insert("", "end", values=(
                entry["date"],
                entry["temperature"],
                entry["description"],
                entry["precipitation"]
            ))

    def save_to_json(self):
        with open("weather_diary.json", "w", encoding="utf-8") as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Записи сохранены в weather_diary.json")

    def load_from_json(self):
        try:
            with open("weather_diary.json", "r", encoding="utf-8") as f:
                self.entries = json.load(f)
            self.update_table()
            messagebox.showinfo("Успех", "Записи загружены из weather_diary.json")
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл weather_diary.json не найден.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    root.mainloop()
