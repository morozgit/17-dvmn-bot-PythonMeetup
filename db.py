import sqlite3

import aiosqlite


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute("""
            create table users
            (
                id               INTEGER not null
                    constraint users_pk
                        primary key autoincrement,
                user_telegram_id INTEGER,
                user_name        INTEGER,
                isAdmin          INTEGER,
                isSpeaker        INTEGER,
                isOrganizer      INTEGER
            );        
        """)
        self.cursor.execute()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_telegram_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_telegram_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_telegram_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def get_active_meetups(self):
        result = self.cursor.execute("SELECT `id`, `name` FROM `meetups` WHERE `is_active` = ?", (1,))
        return bool(len(result.fetchall()))

    def add_new_meetup(self, name):
        result = self.cursor.execute("INSERT INTO `meetups` (`name`, `is_active`) VALUES (?, 1)", (name,))
        return self.conn.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()