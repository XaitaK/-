import psycopg2
from datetime import date
import logging

DB_CONFIG = {
    "host": "localhost",
    "port": "5433",
    "database": "postgres",
    "user": "postgres",
    "password": "2288"
}

TEAMS = [
    (1, 'Динамо', 'Москва', 'Сергей Иванов'),
    (2, 'Спартак', 'Москва', 'Олег Романцев'),
    (3, 'Зенит', 'Санкт-Петербург', 'Сергей Семак'),
    (4, 'ЦСКА', 'Москва', 'Владимир Федотов'),
    (5, 'Краснодар', 'Краснодар', 'Мурад Мусаев'),
    (6, 'Ростов', 'Ростов-на-Дону', 'Валерий Карпин')
]

POSITIONS = ['Вратарь', 'Защитник', 'Полузащитник', 'Нападающий']
ORG_DATA = [
    ('РФС', 'info@rfs.ru'),
    ('Тинькофф', 'support@tinkoff.ru'),
    ('Газпром Спорт', 'contact@gazpromsport.ru')
]

STADIUMS = [
    ('Лужники', 'Москва', 81000),
    ('Открытие Арена', 'Москва', 45360),
    ('Газпром Арена', 'Санкт-Петербург', 68134),
    ('Ростов Арена', 'Ростов-на-Дону', 45000),
    ('Краснодар', 'Краснодар', 35179)
]

REFEREES = [
    ('Сергей Карасев', 'ФИФА'),
    ('Владислав Безбородов', 'Премьер-лига'),
    ('Павел Кукуян', 'Премьер-лига'),
    ('Виктор Каштанов', 'Первая лига')
]

TOURNAMENTS = [
    (1, 'Чемпионат России 2024', 'Лига', '2024-03-01', '2024-11-30', 16),
    (2, 'Кубок России 2024', 'Кубок', '2024-06-01', '2024-07-01', 64),
    (3, 'Суперкубок России 2024', 'Суперкубок', '2024-07-15', '2024-07-15', 2)
]

TOURNAMENT_ORGANIZERS = [
    (1, 1),
    (2, 2),
    (3, 3)
]

USERS = [
    ('admin', 'hashed_password', 'Админ'),
    ('organizer1', 'hashed_password', 'Организатор'),
    ('coach1', 'hashed_password', 'Тренер'),
    ('fan1', 'hashed_password', 'Зритель')
]

MATCHES = [
    (1, 1, 2, 1, 1, '2024-03-10 19:00', 2, 1),
    (1, 3, 4, 3, 2, '2024-03-11 18:00', 1, 1),
    (1, 5, 6, 5, 3, '2024-03-12 17:30', 3, 0),
    (2, 2, 3, 2, 4, '2024-06-05 20:00', 0, 2),
    (2, 4, 5, 4, 1, '2024-06-06 19:30', 1, 1),
    (3, 1, 3, 1, 3, '2024-07-15 21:00', None, None)
]

def generate_players():
    players = []
    player_id = 1

    team_players = {
        'Динамо': [
            'Антон Шуньин', 'Игорь Лещук', 'Роман Евгеньев', 'Дмитрий Скопинцев', 'Саба Сазонов',
            'Денис Макаров', 'Данил Фомин', 'Константин Тюкавин', 'Вячеслав Грулев', 'Сергей Паршивлюк',
            'Александр Кутитладзе', 'Алексей Козлов', 'Артем Самсонов', 'Андрей Мостовой', 'Георгий Кабулов',
            'Дмитрий Беляев', 'Андрей Фролов', 'Максим Петров', 'Виктор Ионов', 'Геннадий Пак',
            'Илья Орлов', 'Никита Артемьев', 'Павел Еремеев', 'Юрий Семин', 'Сергей Юран'
        ],
        'Спартак': [
            'Александр Селихов', 'Георгий Джикия', 'Артем Ребров', 'Роман Зобнин', 'Квинси Промес',
            'Алекс Крал', 'Езекиль Понсе', 'Андрей Ещенко', 'Илья Кутепов', 'Лука Джорджевич',
            'Зелимхан Бакаев', 'Александр Соболев', 'Айртон Лукас', 'Михаил Игнатов', 'Наиль Умяров',
            'Денис Глушаков', 'Павел Маслов', 'Николай Рассказов', 'Александр Максименко', 'Леонид Миронов',
            'Владимир Обухов', 'Сергей Иванов', 'Петр Петров', 'Антон Лосев', 'Федор Черных'
        ],
        'Зенит': [
            'Михаил Кержаков', 'Дуглас Сантос', 'Деян Ловрен', 'Малком', 'Вендел',
            'Алексей Сутормин', 'Сергей Семак', 'Клаудиньо', 'Артем Дзюба', 'Дмитрий Чистяков',
            'Александр Ерохин', 'Юрий Жирков', 'Андрей Лунёв', 'Далер Кузяев', 'Станислав Крицюк',
            'Александр Васютин', 'Дмитрий Васильев', 'Никита Гусев', 'Максим Орлов', 'Павел Морозов',
            'Владислав Смирнов', 'Иван Петров', 'Артем Беляев', 'Владислав Иванов', 'Никита Захаров'
        ],
        'ЦСКА': [
            'Игорь Акинфеев', 'Марио Фернандес', 'Алексей Березуцкий', 'Вадим Карпов', 'Бактиер Зайнутдинов',
            'Константин Кучаев', 'Иван Обляков', 'Алан Дзагоев', 'Чидера Эджуке', 'Фёдор Чалов',
            'Хосе Саломон Рондон', 'Егор Ушаков', 'Кристиян Бистрович', 'Владимир Пискунов', 'Максим Дмитриев',
            'Александр Никифоров', 'Вячеслав Белов', 'Геннадий Орлов', 'Юрий Власов', 'Сергей Громов',
            'Андрей Павлов', 'Артем Кузьмин', 'Илья Белый', 'Виктор Петров', 'Андрей Зайцев'
        ],
        'Краснодар': [
            'Матвей Сафонов', 'Александр Мартынович', 'Сергей Петров', 'Кристиан Рамирес', 'Виктор Классон',
            'Тонни де Вильена', 'Жоаозиньо', 'Джон Кордоба', 'Александр Черников', 'Александр Городов',
            'Реми Кабелла', 'Юрий Газинский', 'Кайо', 'Иван Игнатьев', 'Эдуард Сперцян',
            'Евгений Чернов', 'Андрей Яковлев', 'Максим Фомин', 'Илья Соловьев', 'Дмитрий Ковалев',
            'Георгий Титов', 'Алексей Орлов', 'Владимир Лебедев', 'Николай Долгов', 'Даниил Журавлев'
        ],
        'Ростов': [
            'Егор Бабурин', 'Максим Осипенко', 'Даниил Глебов', 'Никита Медведев', 'Алексей Козлов',
            'Кирилл Божко', 'Игорь Калинин', 'Дмитрий Полоз', 'Александр Сапета', 'Артем Шомко',
            'Виталий Устинов', 'Роман Еременко', 'Бактиер Зайнутдинов', 'Павел Мамаев', 'Андрей Лангович',
            'Дмитрий Чайковский', 'Владимир Быков', 'Антон Егоров', 'Иван Фролов', 'Геннадий Степанов',
            'Артем Артамонов', 'Денис Зайцев', 'Николай Михайлов', 'Сергей Афанасьев', 'Максим Широков'
        ]
    }

    POSITIONS = ['Вратарь', 'Защитник', 'Полузащитник', 'Нападающий']

    for team_id, team_name, _, _ in TEAMS:
        for i in range(25):  # 25 игроков на команду
            full_name = team_players[team_name][i]
            birth_date = date(1995 + (player_id % 5), (player_id % 12) + 1, (player_id % 28) + 1)
            position = POSITIONS[i % 4]
            number = i + 1
            goals = player_id % 5
            yellow_cards = player_id % 3
            red_cards = player_id % 2

            players.append((
                full_name, birth_date, position, number, team_id, goals, yellow_cards, red_cards
            ))
            player_id += 1

    return players

def insert_test_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.executemany("INSERT INTO users (username, password, role) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING", USERS)
        cur.executemany("INSERT INTO teams (id, name, city, coach_name) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING", TEAMS)
        cur.executemany("INSERT INTO organizers (full_name, contact) VALUES (%s, %s) ON CONFLICT DO NOTHING", ORG_DATA)
        cur.executemany("INSERT INTO stadiums (name, city, capacity) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING", STADIUMS)
        cur.executemany("INSERT INTO referees (full_name, category) VALUES (%s, %s) ON CONFLICT DO NOTHING", REFEREES)
        cur.executemany("INSERT INTO tournaments (id, name, type, start_date, end_date, max_teams) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING", TOURNAMENTS)
        cur.executemany("INSERT INTO tournament_organizers (tournament_id, organizer_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", TOURNAMENT_ORGANIZERS)

        # Привязка команд к турнирам
        for tournament_id, _, _, _, _, _ in TOURNAMENTS:
            for team_id, _, _, _ in TEAMS:
                cur.execute("INSERT INTO tournament_teams (tournament_id, team_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (tournament_id, team_id))

        # Игроки
        players = generate_players()
        for p in players:
            cur.execute("""
                INSERT INTO players 
                (full_name, birth_date, position, number, team_id, goals, yellow_cards, red_cards)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, p)

        # Матчи
        for m in MATCHES:
            cur.execute("""
                INSERT INTO matches 
                (tournament_id, home_team_id, away_team_id, stadium_id, referee_id, match_date, home_score, away_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, m)

        conn.commit()
        print("✅ Все тестовые данные успешно добавлены.")

    except Exception as e:
        print("❌ Ошибка при вставке данных:", e)

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    insert_test_data()


