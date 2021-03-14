import requests
import json
import sqlite3
import logging
from Compare import Compare


log = 'log.txt'
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s',
                    level = logging.INFO, filename=log)


class DailyLog:
    """ Класс для получения логов.
        На вход принимает дату, log_date: str.
        Формате даты: год, месяц, день без пробелов.
        Пример: '20210123' """

    def __init__(self, log_date):
        """ Атрибуты класса:
            log_date : str - дата для получения логов(20210123)
            log : list - полученные логи в виде списка, до вызова метода
                         parse_json - пустой
            sorted_log : list - полученные логи в виде отсортированного
                                по времени сообщения списка, до вызова
                                метода sort_log - пустой
            """
        self.log_date = log_date
        self.log = []
        self.sorted_log = []

    def parse_json(self):
        """ Метод для получения логов """
        url = 'http://www.dsdev.tech/logs/' + self.log_date
        try:
            response = requests.get(url).text
            logging.info(f'Получены логи за {self.log_date}')
        except Exception as e:
            logging.critical(f'Ошибка получения логов - {str(e)}')
            return str(e)
        try:
            logs = json.loads(response)['logs']
            self.log = logs
            logging.info(f'Логи сохранены')
        except:
            error = json.loads(response)['error']
            return error
            logging.critical(f'Ошибка сохранения логов - {str(error)}')


    def load_to_db(self):
        """ Метод для записи логов в БД """
        try:
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            for item in self.log:
                log_message = (item['user_id'], item['first_name'],
                               item['second_name'], item['message'],
                               item['created_at'])
                cursor.execute("""INSERT INTO "logs" VALUES (?, ?, ?, ?, ?)""",
                               log_message)
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            return f'Ошибка записи в БД:  + {str(e)}'

    def __merge(self, left, right):
        """ Метод для сортировки полученных логов """
        if len(left) == 0:
            return right
        if len(right) == 0:
            return left
        result = []
        index_left = index_right = 0
        while len(result) < len(left) + len(right):
            if Compare(left[index_left]) <= Compare(right[index_right]):
                result.append(left[index_left])
                index_left += 1
            else:
                result.append(right[index_right])
                index_right += 1
            if index_right == len(right):
                result += left[index_left:]
                break
            if index_left == len(left):
                result += right[index_right:]
                break
        return result

    def __sort(self, array):
        """ Метод для сортировки полученных логов """
        if len(array) < 2:
            return array
        midpoint = len(array) // 2
        return self.__merge(left=self.__sort(array[:midpoint]),
                            right=self.__sort(array[midpoint:]))

    def sort_log(self):
        """ Метод для сортировки полученных логов """
        array = self.log
        self.sorted_log = self.__sort(array)
