import requests
import json
import sqlite3
from Compare import Compare


class LogMessage:
    def __init__(self, log_date):
        self.log_date = log_date
        self.log = []

    def parse_json(self):
        url = 'http://www.dsdev.tech/logs/' + self.log_date
        response = requests.get(url).text
        logs = json.loads(response)['logs']
        self.log = logs

    def load_to_db(self):
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

    def __sort(self, array):
        less = []
        equal = []
        greater = []
        if len(array) > 1:
            pivot = array[0]
            for x in array:
                if Compare(x) < Compare(pivot):
                    less.append(x)
                elif Compare(x) == Compare(pivot):
                    equal.append(x)
                elif Compare(x) > Compare(pivot):
                    greater.append(x)
            return self.__sort(less) + equal + self.__sort(greater)
        else:
            return array

    def sort_log(self):
        array = self.log
        self.log = self.__sort(array)
