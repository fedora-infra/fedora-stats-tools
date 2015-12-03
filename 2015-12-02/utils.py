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

badge_tags_cache = {}
def badge2tags(badge_id):
    if badge_id not in badge_tags_cache:
        url = 'https://badges.fedoraproject.org/badge/%s/json' % badge_id
        response = requests.get(url)
        data = response.json()
        tags = (data['tags'] or '').strip(',').split(',')
        badge_tags_cache[badge_id] = tags
    return badge_tags_cache[badge_id]

