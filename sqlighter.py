import sqlite3

class SQLighter:
    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status = True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            res = self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()
            users = []
            for i in range(len(res)):
                users.append(res[i][1])
            return users

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status = True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def get_messages(self, status = True):
        with self.connection:
            res = self.cursor.execute("SELECT * FROM `messages` WHERE `status` = ?", (status,)).fetchall()
            messages = []
            for i in range(len(res)):
                messages.append(res[i][1])
            return messages

    def update_days(self, user_id, days):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `days` = ? WHERE `user_id` = ?", (days, user_id))

    def get_days(self, status = True):
        with self.connection:
            res = self.cursor.execute("SELECT * FROM `subscriptions` WHERE `days` = ?", (days,)).fetchall()
            days = []
            for i in range(len(res)):
                days.append(res[i][1])
            return days

    def delete_first(self):
        with self.connection:
            self.cursor.execute("DELETE FROM `messages` WHERE rowid = (SELECT MIN(rowid) FROM `messages`)")


    def add_message(self, message, status = True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `messages` (`message`, `status`) VALUES(?,?)", (message,status))


    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
