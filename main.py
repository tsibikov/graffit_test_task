import requests
import json


def get_logs(log_date):
    url = 'http://www.dsdev.tech/logs/' + log_date
    response = requests.get(url).text
    logs = json.loads(response)
    return logs

log_date = '20210123'
logs = get_logs(log_date)



