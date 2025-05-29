import psycopg2

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5433",  # <- обязательно укажи именно этот порт!
        database="postgres",
        user="postgres",
        password="2288"
    )
    print("✅ Подключение к PostgreSQL прошло успешно!")

    # Пример: создадим таблицу
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100)
        );
    ''')
    connection.commit()
    print("📝 Таблица создана или уже существует.")

except Exception as error:
    print("❌ Ошибка подключения:", error)

finally:
    if 'connection' in locals() and connection:
        connection.close()
        print("🔌 Соединение закрыто.")
