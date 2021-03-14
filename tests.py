import unittest
from DailyLog import DailyLog
from Compare import Compare
from unittest.mock import patch, Mock


class TestDailyLog(unittest.TestCase):
    def setUp(self):
        self.logs = DailyLog('20210125')
        self.value = '{"error":"", "logs":[\
            {"created_at": "2021-01-23T13:00:30",\
            "first_name": "Иван",\
            "message": "Some message1",\
            "second_name": "Иванов",\
            "user_id": "77777"},\
            {"created_at": "2021-01-23T12:00:00",\
            "first_name": "Петр",\
            "message": "Some message2",\
            "second_name": "Петров",\
            "user_id": "555555"}]}'

    def test_class_creation(self):
        self.assertEqual(self.logs.log_date, '20210125')
        self.assertEqual(self.logs.log, [])
        self.assertEqual(self.logs.sorted_log, [])

    def test_parse_json(self):
        with patch.object(DailyLog, 'load_json', return_value=self.value):
            self.logs.parse_json()
            name_one = self.logs.log[0]['first_name']
            name_second = self.logs.log[1]['first_name']
            time_one = self.logs.log[0]['created_at']
            message_second = self.logs.log[1]['message']
            self.assertEqual(name_one, 'Иван')
            self.assertEqual(name_second, 'Петр')
            self.assertEqual(time_one, '2021-01-23T13:00:30')
            self.assertEqual(message_second, 'Some message2')

    def test_time_compare(self):
        with patch.object(DailyLog, 'load_json', return_value=self.value):
            self.logs.parse_json()
            log_one = self.logs.log[0]
            log_second = self.logs.log[1]
            result = Compare(log_one) <= Compare(log_second)
            self.assertFalse(result)

    def test_sorting(self):
        with patch.object(DailyLog, 'load_json', return_value=self.value):
            self.logs.parse_json()
            self.logs.sort_log()
            log_one = self.logs.sorted_log[0]
            log_second = self.logs.sorted_log[1]
            result = Compare(log_one) <= Compare(log_second)
            self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
