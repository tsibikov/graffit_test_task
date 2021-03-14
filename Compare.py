class Compare:
    """ Класс для сравнения времени сообщения.
        На вход принимает один элемент из полученного лога.
        Пример:
        {
        "сreated_at": "2021-01-23T12:33:14" — дата создания в формате ISO 8601,
         "first_name": "Матвей" - имя пользователя,
         "message": "Some message" - фраза пользователя,
         "second_name": "Иванов" - фамилия пользователя,
         "user_id": "726462" — ID пользователя
         }"""

    def __init__(self, log_item):
        """ Атрибуты класса:
            time : str - время сообщения(12:33:14)
            hour : int - час(12)
            minute : int - минуты(33)
            second : int - секунды(14)
            """
        self.time = log_item['created_at'][-8:]
        self.hour = int(self.time[:2])
        self.minute = int(self.time[3:5])
        self.second = int(self.time[6:])

    def __le__(self, other):
        """ Метод переопределяет поведение оператора меньше или равно, <= """
        if self.hour != other.hour:
            return self.hour < other.hour
        elif self.hour == other.hour:
            if self.minute != other.minute:
                return self.minute < other.minute
            return self.second <= other.second
