import tkinter as tk
from tkinter import ttk
import sqlite3

# ГЛАВНОЕ ОКНО

# Класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Создание и работа с главным окном
    def init_main(self):
        # Панель инструментов
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        # Упаковка панели
        toolbar.pack(side=tk.TOP, fill=tk.X)

    #КНОПКИ:

        # Добавление
        # Задаем иконку, помещаем в левую сторону экрана:
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_add = tk.Button(toolbar, bg='#d7d7d7', bd=1,
                            image=self.add_img, command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        # Обновление
        self.upd_img = tk.PhotoImage(file='./img/update.png')
        btn_upd = tk.Button(toolbar, bg='#d7d7d7', bd=1,
                            image=self.upd_img, command=self.open_update_dialog)
        btn_upd.pack(side=tk.LEFT)

        # Удаление
        self.del_img = tk.PhotoImage(file='./img/delete.png')
        btn_del = tk.Button(toolbar, bg='#d7d7d7', bd=1,
                            image=self.del_img, command=self.delete_records)
        btn_del.pack(side=tk.LEFT)

        # Поиск
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d7d7', bd=1, 
                               image=self.search_img, command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        # Обновление
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d7d7', bd=1,
                                image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

# СОЗДАНИЕ ТАБЛИЦЫ

        # Добавляем стобцы
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'phone', 'email'),
                                 height=45,show='headings')
        
        # Добавляем параметры колонкам
        self.tree.column('ID', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)

        # Подписываем колонки
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')

        # Упаковка
        self.tree.pack(side=tk.LEFT)

# ВСЕ МЕТОДЫ

    # Добавление данных
    def records(self, name, phone, email):
        self.db.insert_data(name, phone, email)
        self.view_records()

    # Отображение данных в TreeView
    def view_records(self):
        self.db.cur.execute(""" SELECT * FROM users """)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.cur.fetchall()]
        
    # Метод изменения данных
    def update_record(self, name, phone, email):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute(""" UPDATE users SET name=?, phone=?, email=? WHERE ID=? """,
                            (name, phone, email, id))
        self.db.conn.commit()
        self.view_records()

    # Метод для удаления данных
    def delete_records(self):
        for row in self.tree.selection():
            self.db.cur.execute(""" DELETE FROM users WHERE ID=?""", 
                                (self.tree.set(row, '#1')))
        self.db.conn.commit()
        self.view_records()

    # Метод поиска данных
    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.cur.execute(""" SELECT * FROM users WHERE name LIKE ?""", (name, ))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.cur.fetchall()]
        
        # ВЫЗОВ КЛАССОВ

    # Метод, вызывающий окно добавления
    def open_child(self):
        Child()

    # Метод, вызывающий окно обновления
    def open_update_dialog(self):
        Update()

    # Метод, вызывающий окно поиска
    def open_search(self):
        Search()

# СОЗДАНИЕ ОКНА ДОБАВЛЕНИЯ

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Задаем параметры окну
    def init_child(self):
        self.title('Добавить контакт')
        self.geometry('400x220')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        # Задаем текст виджетов ввода и их расположение
        label_name = tk.Label(self, text='ФИО: ')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон ')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail: ')
        label_email.place(x=50, y=110)

        # Прописываем сами виджеты и их расположение
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)

        # Кнопка добавления (подписываем и задаем размеры)
        self.btn_add = ttk.Button(self, text='Добавить')
        self.btn_add.place(x=220, y=170)

        # Фиксируем, что кнопка активируется только при нажатии левой кнопной мыши
        self.btn_add.bind('<Button-1>', lambda event:
                          self.view.records(self.entry_name.get(),
                                            self.entry_phone.get(),
                                            self.entry_email.get()))


        # Кнопка закрытия
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

# ВСЕ КЛАССЫ

# Класс редактирования контактов
class Update(Child):
    def __init__(self):
        super().__init__() 
        self.init_update()
        self.db = db 
        self.default_data()

    def init_update(self):
        self.title('Редактировать позицию')
        self.btn_add.destroy()

        self.btn_upd = ttk.Button(self, text='Редактировать')
        self.btn_upd.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_upd.place(x=200, y=170)

    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute(""" SELECT * FROM users WHERE ID=? """, (id, ))

        # Получение первой записи
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])

# Класс поиска контакта
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск по контактам')
        self.geometry('300x100')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=20, y=20)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=70, y=20)
    
        # Кнопка поиска 
        self.btn_search = ttk.Button(self, text='Найти')
        self.btn_search.place(x=70, y=70)
        self.btn_search.bind('<Button-1>', lambda event:
                             self.view.search_records(self.entry_name.get()))
        self.btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

# Класс базы данных
class DB:
    def __init__(self):
        # Создаем соединение с бд
        self.conn = sqlite3.connect('contacts.db')
        self.cur = self.conn.cursor()
        # Создаем таблицу в бд
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS users(
                                ID INTEGER PRIMARY KEY NOT NULL,
                                name TEXT,
                                phone TEXT,
                                email TEXT)""")
        self.conn.commit()
    # Позволяем добавлять данные с помощью окна добавления
    def insert_data(self, name, phone, email):
        self.cur.execute(""" INSERT INTO users (name, phone, email)
                        VALUES (?, ?, ?)""", (name, phone, email))
        self.conn.commit()

# ВЫЗОВ ПРОГРАММЫ
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Телефонная книга')
    root.geometry('645x450')
    root.resizable(False, False)
    root.configure(bg='White')
    root.mainloop()