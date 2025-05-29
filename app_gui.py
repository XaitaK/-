import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging
from contextlib import contextmanager
from datetime import datetime


# Константы стилей
BG_COLOR = "#F0F0F0"
PRIMARY_COLOR = "#2C3E50"
SECONDARY_COLOR = "#3498DB"
ACCENT_COLOR = "#E74C3C"

logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5433",
        database="postgres",
        user="postgres",
        password="2288"
    )

@contextmanager
def db_connection():
    conn = None
    try:
        conn = get_connection()
        yield conn
    except psycopg2.Error as e:
        logging.error(f"Database error: {e}")
        messagebox.showerror("Ошибка базы данных", str(e))
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        messagebox.showerror("Неизвестная ошибка", str(e))
    finally:
        if conn:
            conn.close()

def clear_listbox(listbox):
    listbox.delete(0, tk.END)

def clear_treeview(treeview):
    for item in treeview.get_children():
        treeview.delete(item)

# Основное окно
root = tk.Tk()
root.title("Футбольные Соревнования")
root.geometry("1400x850")
root.configure(bg=BG_COLOR)

# Стили
style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background=BG_COLOR)
style.configure("TFrame", background=BG_COLOR)
style.configure("TButton", font=("Arial", 10), padding=6, background=SECONDARY_COLOR, foreground="white")
style.map("TButton", background=[("active", PRIMARY_COLOR)])

# Блокнот для вкладок
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

# Вкладка "Команды" -----------------------------------------------------------------
teams_frame = ttk.Frame(notebook)
notebook.add(teams_frame, text=" Команды ")

# Панель управления
team_controls = ttk.Frame(teams_frame)
team_controls.pack(pady=10, fill='x')

# Основное содержимое
teams_content = ttk.Frame(teams_frame)
teams_content.pack(fill='both', expand=True, padx=10)

# Список команд
team_listbox = tk.Listbox(teams_content, width=40, font=("Arial", 11), 
                         bg="white", relief=tk.FLAT, highlightthickness=0)
team_listbox.pack(side=tk.LEFT, fill='y', pady=10, expand=False)

# Скроллбар для списка команд
team_scrollbar = ttk.Scrollbar(teams_content, orient=tk.VERTICAL, command=team_listbox.yview)
team_listbox.configure(yscrollcommand=team_scrollbar.set)
team_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

# Список игроков
players_label = ttk.Label(teams_content, text="Игроки выбранной команды:", 
                         background=BG_COLOR, font=("Arial", 11, "bold"))
players_label.pack(side=tk.TOP, anchor="nw", padx=20, pady=(10,0))

players_listbox = tk.Listbox(teams_content, width=60, font=("Arial", 11), 
                            bg="white", relief=tk.FLAT, highlightthickness=0)
players_listbox.pack(side=tk.LEFT, fill='both', expand=True, padx=20, pady=10)

# Вкладка "Матчи" -------------------------------------------------------------------
matches_frame = ttk.Frame(notebook)
notebook.add(matches_frame, text=" Матчи ")

# Вложенный блокнот для матчей
matches_notebook = ttk.Notebook(matches_frame)
matches_notebook.pack(fill='both', expand=True, padx=10, pady=10)

# Прошедшие матчи
past_matches_tab = ttk.Frame(matches_notebook)
matches_notebook.add(past_matches_tab, text="Прошедшие матчи")

past_matches_tree = ttk.Treeview(past_matches_tab, 
                                columns=("date", "home_team", "score", "away_team", "tournament", "organizer"), 
                                show="headings", height=12)
columns = [
    ("date", "Дата и время", 150),
    ("home_team", "Хозяева", 180),
    ("score", "Счет", 80),
    ("away_team", "Гости", 180),
    ("tournament", "Турнир", 180),
    ("organizer", "Организатор", 180)
]

for col, txt, w in columns:
    past_matches_tree.heading(col, text=txt)
    past_matches_tree.column(col, width=w, anchor=tk.CENTER if col == "score" else tk.W)
past_matches_tree.pack(fill='both', expand=True, padx=5, pady=5, side=tk.LEFT)

past_matches_scrollbar = ttk.Scrollbar(past_matches_tab, orient=tk.VERTICAL, command=past_matches_tree.yview)
past_matches_tree.configure(yscrollcommand=past_matches_scrollbar.set)
past_matches_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Будущие матчи
future_matches_tab = ttk.Frame(matches_notebook)
matches_notebook.add(future_matches_tab, text="Будущие матчи")

columns = [
    ("date", "Дата и время", 150),
    ("home_team", "Хозяева", 150),
    ("score", "Счёт", 60),
    ("away_team", "Гости", 150),
    ("tournament", "Турнир", 150),
    ("organizer", "Организатор", 120)
]

future_matches_tree = ttk.Treeview(
    future_matches_tab,
    columns=[col[0] for col in columns],
    show="headings",
    height=12
)

for col, txt, w in columns:
    future_matches_tree.heading(col, text=txt)
    future_matches_tree.column(col, width=w, anchor=tk.CENTER if col == "score" else tk.W)

future_matches_tree.pack(fill='both', expand=True, padx=5, pady=5, side=tk.LEFT)

# Scrollbar
future_matches_scrollbar = ttk.Scrollbar(future_matches_tab, orient=tk.VERTICAL, command=future_matches_tree.yview)
future_matches_tree.configure(yscrollcommand=future_matches_scrollbar.set)
future_matches_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Аналитика матчей
matches_analytics_tab = ttk.Frame(matches_notebook)
matches_notebook.add(matches_analytics_tab, text="Аналитика")

matches_analytics_label = ttk.Label(matches_analytics_tab, text="", 
                                   background=BG_COLOR, font=("Arial", 12))
matches_analytics_label.pack(anchor="nw", padx=10, pady=10)

# Вкладка "Аналитика" ---------------------------------------------------------------
analytics_frame = ttk.Frame(notebook)
notebook.add(analytics_frame, text=" Аналитика ")

analytics_controls = ttk.Frame(analytics_frame)
analytics_controls.pack(pady=10, fill='x')

chart_frame = ttk.Frame(analytics_frame)
chart_frame.pack(fill='both', expand=True, padx=10, pady=10)

# Функции ---------------------------------------------------------------------------
def show_teams():
    clear_listbox(team_listbox)
    with db_connection() as conn:
        if conn is None:
            messagebox.showerror("Ошибка", "Не удалось подключиться к БД")
            return
        cur = conn.cursor()
        cur.execute("SELECT id, name, city, coach_name FROM teams ORDER BY name")
        rows = cur.fetchall()
        for row in rows:
            team_listbox.insert(tk.END, f"{row[1]} | Город: {row[2]} | Тренер: {row[3]}")
        team_listbox.team_ids = [row[0] for row in rows]

def show_players_for_team(event=None):
    clear_listbox(players_listbox)
    selection = team_listbox.curselection()
    if not selection:
        return
    team_index = selection[0]
    team_id = team_listbox.team_ids[team_index]
    with db_connection() as conn:
        if conn is None:
            return
        cur = conn.cursor()
        cur.execute("""
            SELECT full_name, birth_date, position, number, goals, yellow_cards, red_cards
            FROM players
            WHERE team_id = %s
            ORDER BY position, full_name
        """, (team_id,))
        for row in cur.fetchall():
            birth_date_str = row[1].strftime("%d.%m.%Y")
            players_listbox.insert(
                tk.END,
                f"{row[0]} | ДР: {birth_date_str} | Позиция: {row[2]} | №{row[3]} | Голы: {row[4]} | ЖК: {row[5]} | КК: {row[6]}"
            )

def show_past_matches():
    clear_treeview(past_matches_tree)
    with get_connection() as conn:
        if conn is None:
            return
        cur = conn.cursor()
        cur.execute("""
            SELECT m.match_date, ht.name, m.home_score, m.away_score, at.name, 
                   tr.name, COALESCE(tor.organizers, '')
            FROM matches m
            JOIN teams ht ON m.home_team_id = ht.id
            JOIN teams at ON m.away_team_id = at.id
            JOIN tournaments tr ON m.tournament_id = tr.id
            LEFT JOIN (
                SELECT tor.tournament_id, 
                       STRING_AGG(org.full_name, ', ') AS organizers
                FROM tournament_organizers tor
                LEFT JOIN organizers org ON tor.organizer_id = org.id
                GROUP BY tor.tournament_id
            ) AS tor ON tr.id = tor.tournament_id
            WHERE m.match_date < NOW()
            ORDER BY m.match_date DESC
        """)
        for row in cur.fetchall():
            date = row[0].strftime("%d.%m.%Y %H:%M")
            score = f"{row[2]} - {row[3]}"
            past_matches_tree.insert("", tk.END, values=(date, row[1], score, row[4], row[5], row[6]))

def show_future_matches():
    clear_treeview(future_matches_tree)
    with db_connection() as conn:
        if conn is None:
            return
        cur = conn.cursor()
        cur.execute("""
            SELECT m.match_date, ht.name, m.home_score, m.away_score, at.name, 
                   tr.name, COALESCE(tor.organizers, '')
            FROM matches m
            JOIN teams ht ON m.home_team_id = ht.id
            JOIN teams at ON m.away_team_id = at.id
            JOIN tournaments tr ON m.tournament_id = tr.id
            LEFT JOIN (
                SELECT tor.tournament_id, 
                       STRING_AGG(org.full_name, ', ') AS organizers
                FROM tournament_organizers tor
                LEFT JOIN organizers org ON tor.organizer_id = org.id
                GROUP BY tor.tournament_id
            ) AS tor ON tr.id = tor.tournament_id
            WHERE m.match_date >= NOW()
            ORDER BY m.match_date ASC
        """)
        for row in cur.fetchall():
            date = row[0].strftime("%d.%m.%Y %H:%M")
            score = f"{row[2] if row[2] is not None else '-'} - {row[3] if row[3] is not None else '-'}"
            future_matches_tree.insert("", tk.END, values=(date, row[1], score, row[4], row[5], row[6]))

def show_matches_analytics():
    with db_connection() as conn:
        if conn is None:
            matches_analytics_label.config(text="Нет данных")
            return
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM matches")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM matches WHERE match_date < NOW()")
        past = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM matches WHERE match_date >= NOW()")
        future = cur.fetchone()[0]
        cur.execute("""
            SELECT AVG(home_score + away_score) 
            FROM matches 
            WHERE home_score IS NOT NULL AND away_score IS NOT NULL
        """)
        avg_score = cur.fetchone()[0]
        
        avg_score_text = f"{avg_score:.2f}" if avg_score is not None else "Нет данных по счету"
        text = (
            f"Всего матчей: {total}\n"
            f"Прошедших матчей: {past}\n"
            f"Будущих матчей: {future}\n"
            f"Средний суммарный счет: {avg_score_text}"
        )
        matches_analytics_label.config(text=text)

def show_player_stats():
    clear_chart()
    with db_connection() as conn:
        if conn is None:
            return
        cur = conn.cursor()
        cur.execute("""
            SELECT full_name, goals 
            FROM players 
            ORDER BY goals DESC 
            LIMIT 5
        """)
        data = cur.fetchall()
        fig, ax = plt.subplots(figsize=(8, 4))
        names = [row[0] for row in data]
        goals = [row[1] for row in data]
        bars = ax.barh(names, goals, color=SECONDARY_COLOR)
        ax.bar_label(bars, padding=5)
        ax.set_title('Топ 5 бомбардиров', fontsize=12, pad=15)
        ax.set_facecolor(BG_COLOR)
        fig.patch.set_facecolor(BG_COLOR)
        embed_chart(fig)

def show_team_stats():
    clear_chart()
    with db_connection() as conn:
        if conn is None:
            return
        cur = conn.cursor()
        cur.execute("""
            SELECT t.name, 
                   SUM(CASE 
                       WHEN (m.home_team_id = t.id AND m.home_score > m.away_score) OR 
                            (m.away_team_id = t.id AND m.away_score > m.home_score) 
                       THEN 1 ELSE 0 
                   END) as wins
            FROM teams t
            LEFT JOIN matches m ON t.id = m.home_team_id OR t.id = m.away_team_id
            GROUP BY t.name
            ORDER BY wins DESC
        """)
        data = cur.fetchall()
        fig, ax = plt.subplots(figsize=(8, 4))
        teams = [row[0] for row in data]
        wins = [row[1] for row in data]
        bars = ax.bar(teams, wins, color=ACCENT_COLOR)
        ax.bar_label(bars, padding=5)
        ax.set_title('Победы по командам', fontsize=12, pad=15)
        ax.set_xticks(range(len(teams)))
        ax.set_xticklabels(teams, rotation=45, ha='right')
        ax.grid(alpha=0.3)
        fig.patch.set_facecolor(BG_COLOR)
        embed_chart(fig)

def embed_chart(fig):
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def clear_chart():
    for widget in chart_frame.winfo_children():
        widget.destroy()

# Конфигурация базы данных
DB_CONFIG = {
    "host": "localhost",
    "port": "5433",
    "database": "postgres",
    "user": "postgres",
    "password": "2288"
}

# Цвет фона
BG_COLOR = "#f0f0f0"

# Функция подключения к базе
def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# Окно вывода будущих матчей
def open_future_matches_window():
    matches_window = tk.Toplevel()
    matches_window.title("Будущие матчи")
    matches_window.geometry("800x400")
    matches_window.configure(bg=BG_COLOR)

    columns = [
        ("date", "Дата", 140),
        ("home_team", "Хозяева", 150),
        ("score", "Счёт", 70),
        ("away_team", "Гости", 150),
        ("tournament", "Турнир", 120),
        ("organizer", "Организатор", 120)
    ]

    tree = ttk.Treeview(matches_window, columns=[col[0] for col in columns],
                        show="headings", height=12)

    for col, txt, w in columns:
        tree.heading(col, text=txt)
        tree.column(col, width=w, anchor=tk.CENTER if col == "score" else tk.W)

    tree.pack(fill='both', expand=True, padx=5, pady=5, side=tk.LEFT)

    scrollbar = ttk.Scrollbar(matches_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Функция загрузки будущих матчей в таблицу
    def show_future_matches():
        for item in tree.get_children():
            tree.delete(item)

        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                SELECT m.match_date, 
                       t1.name AS home_team, 
                       t2.name AS away_team, 
                       tr.name AS tournament_name, 
                       o.full_name AS organizer_name
                FROM matches m
                JOIN teams t1 ON m.home_team_id = t1.id
                JOIN teams t2 ON m.away_team_id = t2.id
                JOIN tournaments tr ON m.tournament_id = tr.id
                LEFT JOIN tournament_organizers tor ON tor.tournament_id = tr.id
                LEFT JOIN organizers o ON tor.organizer_id = o.id
                WHERE m.match_date > NOW()
                ORDER BY m.match_date
            """)

            rows = cur.fetchall()

            for row in rows:
                match_date = row[0].strftime("%Y-%m-%d %H:%M")
                home_team = row[1]
                away_team = row[2]
                tournament = row[3]
                organizer = row[4] if row[4] else "—"
                score = "— : —"
                tree.insert("", "end", values=(match_date, home_team, score, away_team, tournament, organizer))

            conn.close()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить будущие матчи: {e}")

    show_future_matches()

    # Кнопка "Добавить матч"
    add_match_button = tk.Button(matches_window, text="Добавить матч",
                                 command=lambda: open_add_match_window(matches_window, show_future_matches))
    add_match_button.pack(pady=10)

# Окно добавления будущего матча
def open_add_match_window(root, on_add_callback):
    add_window = tk.Toplevel(root)
    add_window.title("Добавить будущий матч")
    add_window.geometry("400x400")
    add_window.configure(bg=BG_COLOR)

    ttk.Label(add_window, text="Дата и время (ГГГГ-ММ-ДД ЧЧ:ММ):", background=BG_COLOR).pack(pady=5)
    entry_date = ttk.Entry(add_window)
    entry_date.pack(pady=5)

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM teams")
        teams = cur.fetchall()
        cur.execute("SELECT id, name FROM tournaments")
        tournaments = cur.fetchall()

    team_names = [team[1] for team in teams]
    tournament_names = [t[1] for t in tournaments]

    ttk.Label(add_window, text="Хозяева:", background=BG_COLOR).pack(pady=5)
    home_team_cb = ttk.Combobox(add_window, values=team_names, state="readonly")
    home_team_cb.pack(pady=5)

    ttk.Label(add_window, text="Гости:", background=BG_COLOR).pack(pady=5)
    away_team_cb = ttk.Combobox(add_window, values=team_names, state="readonly")
    away_team_cb.pack(pady=5)

    ttk.Label(add_window, text="Турнир:", background=BG_COLOR).pack(pady=5)
    tournament_cb = ttk.Combobox(add_window, values=tournament_names, state="readonly")
    tournament_cb.pack(pady=5)

    def add_match_to_db():
        date_str = entry_date.get()
        try:
            match_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД ЧЧ:ММ")
            return

        home_team_name = home_team_cb.get()
        away_team_name = away_team_cb.get()
        tournament_name = tournament_cb.get()

        if not (home_team_name and away_team_name and tournament_name):
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        with get_connection() as conn:
            cur = conn.cursor()

            cur.execute("SELECT id FROM teams WHERE name = %s", (home_team_name,))
            home_id = cur.fetchone()[0]

            cur.execute("SELECT id FROM teams WHERE name = %s", (away_team_name,))
            away_id = cur.fetchone()[0]

            cur.execute("SELECT id FROM tournaments WHERE name = %s", (tournament_name,))
            tournament_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO matches (match_date, home_team_id, away_team_id, tournament_id)
                VALUES (%s, %s, %s, %s)
            """, (match_date, home_id, away_id, tournament_id))

            conn.commit()

        messagebox.showinfo("Успех", "Матч добавлен!")
        add_window.destroy()
        on_add_callback()

    ttk.Button(add_window, text="Добавить матч", command=add_match_to_db).pack(pady=15)

# Главное меню
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Меню")
    root.geometry("300x200")
    root.configure(bg=BG_COLOR)

    # Кнопка добавления матча с правильной передачей аргументов
    ttk.Button(root, text="Добавить матч", command=lambda: open_add_match_window(root, show_future_matches)).pack(pady=50)




# Привязки и кнопки -----------------------------------------------------------------
team_listbox.bind("<<ListboxSelect>>", show_players_for_team)

btn_show_teams = ttk.Button(team_controls, text="Обновить список", command=show_teams)
btn_show_teams.pack(side=tk.LEFT, padx=5)

btn_show_past_matches = ttk.Button(past_matches_tab, text="Обновить прошедшие матчи", command=show_past_matches)
btn_show_past_matches.pack(anchor="nw", padx=5, pady=5)

btn_show_future_matches = ttk.Button(future_matches_tab, text="Обновить будущие матчи", command=show_future_matches)
btn_show_future_matches.pack(anchor="nw", padx=5, pady=5)

btn_show_matches_analytics = ttk.Button(matches_analytics_tab, text="Показать аналитику", command=show_matches_analytics)
btn_show_matches_analytics.pack(anchor="nw", padx=5, pady=5)

btn_show_stats = ttk.Button(analytics_controls, text="Топ бомбардиры", command=show_player_stats)
btn_show_stats.pack(side=tk.LEFT, padx=5)

btn_show_teams_stats = ttk.Button(analytics_controls, text="Статистика команд", command=show_team_stats)
btn_show_teams_stats.pack(side=tk.LEFT, padx=5)

btn_add_future_match = ttk.Button(future_matches_tab, text="Добавить матч", command=open_add_match_window)
btn_add_future_match.pack(anchor="nw", padx=5, pady=5)


# Инициализация данных --------------------------------------------------------------
show_teams()
show_past_matches()
show_future_matches()
show_matches_analytics()

root.mainloop()