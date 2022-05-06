import sqlite3


class SQLite:
    def __init__(self):
        self.connection = sqlite3.connect('data/database.sqlite')
        self.cursor = self.connection.cursor()

    def create_subsribtions(self):
        """Создаем таблиуц юзеров"""
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS subscriptions(increment INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,"
            "status BOOL, balance INTEGER,user_login CHAR (100))")

    def create_queue(self):
        """создаем таблицу с очередью на парсинг"""
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS queue(tour TEXT)")

    def get_subscriptions(self, status="true"):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            self.cursor.execute("SELECT * FROM subscriptions WHERE status = %s", (status,))
            return self.cursor.fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            self.cursor.execute(f"SELECT * FROM subscriptions WHERE user_id = {user_id}")
            return bool(len(self.cursor.fetchall()))

    def add_subscriber(self, user_id, user_name, status="true"):
        """Добавляем нового подписчика"""

        with self.connection:
            self.cursor.execute(
                f"""INSERT INTO subscriptions (user_id, status, balance, user_login) VALUES({user_id}, {status}, 0, "{user_name}")""")

    def get_user_info(self, user_id):
        """Получение информации по юзеру"""
        with self.connection:
            self.cursor.execute(f"SELECT * FROM subscriptions WHERE user_id = {user_id}")
            return self.cursor.fetchall()

    def update_queue(self, tour):
        with self.connection:
            self.cursor.execute(
                f"""INSERT INTO queue (tour) VALUES("{tour}")""")

    def get_queue(self):
        """Получаем все"""
        with self.connection:
            self.cursor.execute("SELECT * FROM queue")
            return self.cursor.fetchall()

    def clear_queue(self):
        with self.connection:
            self.cursor.execute("DELETE FROM queue")
