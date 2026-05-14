import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

MOVIES_FILE = "movies.json"

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library (Личная кинотека)")
        self.movies = []
        self.filtered_movies = []
        self.load_movies()

        # --- Форма для ввода фильма ---
        frm = tk.Frame(root)
        frm.pack(pady=8)

        tk.Label(frm, text="Название:").grid(row=0, column=0)
        self.title_entry = tk.Entry(frm, width=20)
        self.title_entry.grid(row=0, column=1)

        tk.Label(frm, text="Жанр:").grid(row=0, column=2)
        self.genre_entry = tk.Entry(frm, width=15)
        self.genre_entry.grid(row=0, column=3)

        tk.Label(frm, text="Год:").grid(row=0, column=4)
        self.year_entry = tk.Entry(frm, width=6)
        self.year_entry.grid(row=0, column=5)

        tk.Label(frm, text="Рейтинг (0-10):").grid(row=0, column=6)
        self.rating_entry = tk.Entry(frm, width=5)
        self.rating_entry.grid(row=0, column=7)

        add_btn = tk.Button(frm, text="Добавить фильм", command=self.add_movie)
        add_btn.grid(row=0, column=8, padx=6)

        # --- Фильтр ---
        filter_frm = tk.Frame(root)
        filter_frm.pack(pady=4)
        tk.Label(filter_frm, text="Фильтр по жанру:").pack(side=tk.LEFT)
        self.filter_genre = tk.Entry(filter_frm, width=13)
        self.filter_genre.pack(side=tk.LEFT, padx=2)

        tk.Label(filter_frm, text="Год:").pack(side=tk.LEFT)
        self.filter_year = tk.Entry(filter_frm, width=7)
        self.filter_year.pack(side=tk.LEFT, padx=2)

        filter_btn = tk.Button(filter_frm, text="Фильтровать", command=self.apply_filter)
        filter_btn.pack(side=tk.LEFT, padx=3)

        reset_btn = tk.Button(filter_frm, text="Сбросить", command=self.reset_filter)
        reset_btn.pack(side=tk.LEFT, padx=3)

        # --- Таблица фильмов ---
        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")
        self.tree.pack(pady=6, fill=tk.X)
        self.update_table()

        # --- Кнопки (сохранить/загрузить) ---
        hl_frm = tk.Frame(root)
        hl_frm.pack(pady=2)
        save_btn = tk.Button(hl_frm, text="Сохранить", command=self.save_movies)
        save_btn.pack(side=tk.LEFT, padx=4)
        load_btn = tk.Button(hl_frm, text="Загрузить", command=self.load_movies)
        load_btn.pack(side=tk.LEFT, padx=4)

    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()

        # Проверка данных
        if not title or not genre or not year or not rating:
            messagebox.showwarning("Ошибка", "Заполните все поля.")
            return
        if not year.isdigit() or not (1800 <= int(year) <= 2100):
            messagebox.showwarning("Ошибка", "Год должен быть числом от 1800 до 2100.")
            return
        try:
            rating_f = float(rating)
            if not (0 <= rating_f <= 10):
                raise ValueError
        except Exception:
            messagebox.showwarning("Ошибка", "Рейтинг должен быть числом от 0 до 10.")
            return

        movie = {"title": title, "genre": genre, "year": int(year), "rating": rating_f}
        self.movies.append(movie)
        self.update_table()
        self.save_movies(auto=True)
        # Очистка полей ввода
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def update_table(self):
        self.tree.delete(*self.tree.get_children())
        data = self.filtered_movies if self.filtered_movies else self.movies
        for m in data:
            self.tree.insert("", tk.END, values=(m["title"], m["genre"], m["year"], m["rating"]))

    def apply_filter(self):
        genre = self.filter_genre.get().strip().lower()
        year = self.filter_year.get().strip()
        self.filtered_movies = [
            m for m in self.movies
            if (genre in m["genre"].lower() if genre else True) and
               (str(m["year"]) == year if year else True)
        ]
        self.update_table()

    def reset_filter(self):
        self.filtered_movies = []
        self.update_table()
        self.filter_genre.delete(0, tk.END)
        self.filter_year.delete(0, tk.END)

    def save_movies(self, auto=False):
        try:
            with open(MOVIES_FILE, "w", encoding="utf-8") as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=2)
            if not auto:
                messagebox.showinfo("Сохранено", "Данные сохранены в movies.json.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def load_movies(self):
        if os.path.exists(MOVIES_FILE):
            try:
                with open(MOVIES_FILE, "r", encoding="utf-8") as f:
                    self.movies = json.load(f)
            except Exception:
                self.movies = []
        self.update_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
