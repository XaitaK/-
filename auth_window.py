import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
import subprocess

# Подключение к базе данных
def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5433",
        database="postgres",
        user="postgres",
        password="2288"
    )

# Авторизация пользователя
def login():
    username = entry_username.get()
    password = entry_password.get()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT password, role FROM users WHERE username = %s", (username,))
    result = cur.fetchone()

    if result and result[0] == password:
        role = result[1]
        messagebox.showinfo("Успех", f"Авторизация прошла успешно.\nВаша роль: {role}")
        root.destroy()
        subprocess.Popen(["python", "app_gui.py"])  # Запускаем главное приложение
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")

    conn.close()

# Регистрация нового пользователя
def register():
    username = entry_username.get()
    password = entry_password.get()
    role = combo_role.get()

    if not role:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите роль")
        return

    conn = get_connection()
    cur = conn.cursor()

    # Проверка на существование пользователя
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cur.fetchone():
        messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует")
    else:
        # Добавление нового пользователя с ролью
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, password, role)
        )
        conn.commit()
        messagebox.showinfo("Успех", f"Регистрация прошла успешно с ролью: {role}")

    conn.close()

# Окно авторизации
root = tk.Tk()
root.title("Авторизация")
root.geometry("300x250")

tk.Label(root, text="Логин:").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

tk.Label(root, text="Пароль:").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

tk.Label(root, text="Роль:").pack(pady=5)
combo_role = ttk.Combobox(root, values=["Пользователь", "Тренер", "Организатор", "Админ"])
combo_role.pack(pady=5)

tk.Button(root, text="Войти", command=login).pack(pady=5)
tk.Button(root, text="Зарегистрироваться", command=register).pack(pady=5)

root.mainloop()
