import datetime

import requests

url = 'https://apps.fedoraproject.org/datagrepper/raw'

def grep(**kwargs):
    response = requests.get(url, params=kwargs)
    data = response.json()
    pages = data['pages']

    for message in data['raw_messages']:
        yield message

    for page in range(1, pages):
        kwargs['page'] = page
        response = requests.get(url, params=kwargs)
        data = response.json()
        for message in data['raw_messages']:
            yield message


def monthly_timebucket(timestamp):
    then = datetime.datetime.fromtimestamp(timestamp)
    date = datetime.date(then.year, then.month, 1)
    return date

def daily_timebucket(timestamp):
    then = datetime.datetime.fromtimestamp(timestamp)
    return then.date()
