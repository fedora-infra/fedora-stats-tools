import datetime

import requests

url = 'https://apps.fedoraproject.org/datagrepper/raw'

ignored_badges = [
    'origin',
]


def badge_id(msg):
    return msg['msg'].get('badge', {}).get('badge_id')


def grep(tries=0, **kwargs):
    response = requests.get(url, params=kwargs)
    if not bool(response):
        if tries > 7:
            raise IOError("Failed to %r %r" % (response.url, response))
        for item in grep(tries=tries + 1, **kwargs):
            yield item

    data = response.json()
    pages = data['pages']

    for message in data['raw_messages']:
        if badge_id(message) in ignored_badges:
            continue
        yield message

    for page in range(1, pages):
        kwargs['page'] = page
        response = requests.get(url, params=kwargs)
        try:
            data = response.json()
        except Exception as e:
            if "Expecting value" in str(e):
                continue
            else:
                raise

        for message in data.get('raw_messages', []):
            if badge_id(message) in ignored_badges:
                continue
            yield message


def monthly_timebucket(timestamp):
    then = datetime.datetime.fromtimestamp(timestamp)
    date = datetime.date(then.year, then.month, 1)
    return date

def daily_timebucket(timestamp):
    then = datetime.datetime.fromtimestamp(timestamp)
    return then.date()

def weekly_timebucket(timestamp):
    then = datetime.datetime.fromtimestamp(timestamp)
    calendar = then.isocalendar()
    return str(calendar[0]) + "-" + ("%i" % calendar[1]).zfill(2)

badge_tags_cache = {}
def badge2tags(badge_id):
    if badge_id not in badge_tags_cache:
        url = 'https://badges.fedoraproject.org/badge/%s/json' % badge_id
        response = requests.get(url)
        data = response.json()
        if 'tags' in data:
            tags = (data['tags'] or '').strip(',').split(',')
            badge_tags_cache[badge_id] = tags
        else:
            badge_tags_cache[badge_id] = []

    return badge_tags_cache[badge_id]

