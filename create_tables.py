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

# ... твои списки TEAMS, POSITIONS, ORG_DATA, STADIUMS, REFEREES, TOURNAMENTS, TOURNAMENT_ORGANIZERS, USERS, MATCHES остаются как есть

def clear_test_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Удаляем данные из зависимых таблиц
        cur.execute("DELETE FROM tournament_teams")
        cur.execute("DELETE FROM matches")
        cur.execute("DELETE FROM players")

        # Удаляем данные из основных таблиц
        cur.execute("DELETE FROM tournament_organizers")
        cur.execute("DELETE FROM tournaments")
        cur.execute("DELETE FROM referees")
        cur.execute("DELETE FROM stadiums")
        cur.execute("DELETE FROM organizers")
        cur.execute("DELETE FROM teams")
        cur.execute("DELETE FROM users")

        conn.commit()
        print("🗑️ Старые данные успешно удалены.")

    except Exception as e:
        print("❌ Ошибка при очистке данных:", e)

    finally:
        if conn:
            conn.close()

def generate_players():
    players = []
    player_id = 1

    team_players = {
        # твои списки игроков по командам — без изменений
    }

    POSITIONS = ['Вратарь', 'Защитник', 'Полузащитник', 'Нападающий']

    for team_id, team_name, _, _ in TEAMS:
        for i in range(25):
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

        for tournament_id, _, _, _, _, _ in TOURNAMENTS:
            for team_id, _, _, _ in TEAMS:
                cur.execute("INSERT INTO tournament_teams (tournament_id, team_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (tournament_id, team_id))

        players = generate_players()
        for p in players:
            cur.execute("""
                INSERT INTO players 
                (full_name, birth_date, position, number, team_id, goals, yellow_cards, red_cards)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, p)

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
    clear_test_data()
    insert_test_data()
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

# ... твои списки TEAMS, POSITIONS, ORG_DATA, STADIUMS, REFEREES, TOURNAMENTS, TOURNAMENT_ORGANIZERS, USERS, MATCHES остаются как есть

def clear_test_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Удаляем данные из зависимых таблиц
        cur.execute("DELETE FROM tournament_teams")
        cur.execute("DELETE FROM matches")
        cur.execute("DELETE FROM players")

        # Удаляем данные из основных таблиц
        cur.execute("DELETE FROM tournament_organizers")
        cur.execute("DELETE FROM tournaments")
        cur.execute("DELETE FROM referees")
        cur.execute("DELETE FROM stadiums")
        cur.execute("DELETE FROM organizers")
        cur.execute("DELETE FROM teams")
        cur.execute("DELETE FROM users")

        conn.commit()
        print("🗑️ Старые данные успешно удалены.")

    except Exception as e:
        print("❌ Ошибка при очистке данных:", e)

    finally:
        if conn:
            conn.close()

def generate_players():
    players = []
    player_id = 1

    team_players = {
        # твои списки игроков по командам — без изменений
    }

    POSITIONS = ['Вратарь', 'Защитник', 'Полузащитник', 'Нападающий']

    for team_id, team_name, _, _ in TEAMS:
        for i in range(25):
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

        for tournament_id, _, _, _, _, _ in TOURNAMENTS:
            for team_id, _, _, _ in TEAMS:
                cur.execute("INSERT INTO tournament_teams (tournament_id, team_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (tournament_id, team_id))

        players = generate_players()
        for p in players:
            cur.execute("""
                INSERT INTO players 
                (full_name, birth_date, position, number, team_id, goals, yellow_cards, red_cards)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, p)

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
    clear_test_data()
    insert_test_data()
