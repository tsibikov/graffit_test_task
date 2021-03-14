import sqlite3
import os


def create_db(db_name):
    """ Функция для создания Базы Даных. 
        Таблица - logs.
        Поля - id, user_id, first_name, second_name, message, created_at """
    cur_dir = os.getcwd()
    path_db = os.path.join(cur_dir, db_name)
    if not os.path.exists(path_db):
        try:
            conn = sqlite3.connect(path_db)
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE "logs"(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    first_name TEXT,
                    second_name TEXT,
                    message TEXT,
                    created_at TEXT
                );
            """)
            conn.commit()
            return f'БД успешно создана'
        except sqlite3.Error as e:            
            return f'Ошибка создания БД:  + {str(e)}'


if __name__ == "__main__":
    database_name = 'db.sqlite3'
    print(create_db(database_name))
