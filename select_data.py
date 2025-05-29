import psycopg2

sql_commands = [
    """
    CREATE TABLE IF NOT EXISTS teams (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL,
        city VARCHAR(100),
        coach_name VARCHAR(100)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(100) NOT NULL,
        birth_date DATE NOT NULL,
        position VARCHAR(50),
        number INTEGER,
        team_id INTEGER REFERENCES teams(id),
        goals INTEGER DEFAULT 0,
        yellow_cards INTEGER DEFAULT 0,
        red_cards INTEGER DEFAULT 0,
        CHECK (EXTRACT(YEAR FROM AGE(CURRENT_DATE, birth_date)) >= 16)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS referees (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(100) NOT NULL,
        category VARCHAR(50)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS stadiums (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        city VARCHAR(100),
        capacity INTEGER
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS tournaments (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        type VARCHAR(50),
        start_date DATE,
        end_date DATE,
        max_teams INTEGER
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS matches (
        id SERIAL PRIMARY KEY,
        tournament_id INTEGER REFERENCES tournaments(id),
        home_team_id INTEGER REFERENCES teams(id),
        away_team_id INTEGER REFERENCES teams(id),
        stadium_id INTEGER REFERENCES stadiums(id),
        referee_id INTEGER REFERENCES referees(id),
        match_date TIMESTAMP NOT NULL,
        home_score INTEGER DEFAULT 0,
        away_score INTEGER DEFAULT 0,
        CHECK (home_team_id <> away_team_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS organizers (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(100) NOT NULL,
        contact VARCHAR(100)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS tournament_organizers (
        tournament_id INTEGER REFERENCES tournaments(id) ON DELETE CASCADE,
        organizer_id INTEGER REFERENCES organizers(id) ON DELETE CASCADE,
        PRIMARY KEY (tournament_id, organizer_id)
    );
    """
]

def create_tables():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5433",
            database="postgres",
            user="postgres",
            password="2288"
        )
        cur = conn.cursor()
        for command in sql_commands:
            cur.execute(command)
        conn.commit()
        print("✅ Все таблицы успешно созданы!")
    except Exception as e:
        print("❌ Ошибка при создании таблиц:", e)
    finally:
        if conn:
            conn.close()
            print("🔌 Соединение закрыто.")

if __name__ == "__main__":
    create_tables()
