"""
query is {'topic': 'org.fedoraproject.prod.buildsys.build.state.change'}
---------------
0 years ago 940049
1 years ago 467118
2 years ago 133368
3 years ago 0

query is {'topic': 'org.fedoraproject.prod.buildsys.build.state.change', 'contains': 'primary'}
---------------
0 years ago 296830
1 years ago 121010
2 years ago 0
3 years ago 0

query is {'topic': 'org.fedoraproject.prod.copr.build.end'}
---------------
0 years ago 193176
1 years ago 64285
2 years ago 0
3 years ago 0

query is {'topic': 'org.fedoraproject.prod.bodhi.update.comment'}
---------------
0 years ago 19098
1 years ago 16807
2 years ago 11448
3 years ago 0

query is {'topic': 'org.fedoraproject.prod.bodhi.update.comment', 'contains': '"anonymous":false'}
---------------
0 years ago 18728
1 years ago 16345
2 years ago 7145
3 years ago 0

query is {'topic': 'org.fedoraproject.prod.bodhi.update.comment', 'contains': '"anonymous":true'}
---------------
0 years ago 370
1 years ago 462
2 years ago 230
3 years ago 0

"""

import copy
import time

import requests

one_minute = 60
one_hour = one_minute * 60
one_day = one_hour * 24
one_month = one_day * 30
one_year = one_day * 365

def get_count(start, finish, query):
    query = copy.copy(query)
    query['start'] = start
    query['end'] = end
    response = requests.get(
        'https://apps.fedoraproject.org/datagrepper/raw',
        params=query,
    )
    data = response.json()
    return data['total']

queries = [
    {
        # You have to divide these results by 2 to get the real number
        'topic': 'org.fedoraproject.prod.buildsys.build.state.change',
    },
    {
        # You have to divide these results by 2 to get the real number
        'topic': 'org.fedoraproject.prod.buildsys.build.state.change',
        'contains': 'primary',
    },
    {
        'topic': 'org.fedoraproject.prod.copr.build.end',
    },
    {
        'topic': 'org.fedoraproject.prod.bodhi.update.comment',
    },
    {
        'topic': 'org.fedoraproject.prod.bodhi.update.comment',
        'contains': '"anonymous":false',
    },
    {
        'topic': 'org.fedoraproject.prod.bodhi.update.comment',
        'contains': '"anonymous":true',
    },
]
for query in queries:
    print "query is", query
    print "---------------"
    for year in range(4):
        end = time.time() - one_year * year
        start = time.time() - one_year * (year + 1)
        print "%i years ago" % year,
        print get_count(start, end, query)
    print
