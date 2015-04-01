import collections
import json
import pprint
import time

import requests

import fedmsg.config
import fedmsg.meta

config = fedmsg.config.load_config()
fedmsg.meta.make_processors(**config)

start = time.time()
one_day = 1 * 24 * 60 * 60
whole_range = one_day
N = 50


def get_page(page, end, delta):
    url = 'https://apps.fedoraproject.org/datagrepper/raw'
    response = requests.get(url, params=dict(
        delta=delta,
        page=page,
        end=end,
        rows_per_page=100,
    ))
    data = response.json()
    return data


results = {}
now = time.time()

for iteration, end in enumerate(range(*map(int, (now - whole_range, now, whole_range / N)))):
    results[end] = collections.defaultdict(int)
    data = get_page(1, end, whole_range)
    pages = data['pages']

    for page in range(1, pages + 1):
        print "* (", iteration, ") getting page", page, "of", data['pages'], "with end", end, "and delta", whole_range
        data = get_page(page, end, whole_range)
        messages = data['raw_messages']

        for message in messages:
            users = fedmsg.meta.msg2usernames(message, **config)
            for user in users:
                results[end][user] += 1

    #pprint.pprint(dict(results))

with open('foo.json', 'w') as f:
    f.write(json.dumps(results))
