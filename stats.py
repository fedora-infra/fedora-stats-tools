# Borrowed heavily from thisweekinfedora by pingou, @pypingou

import calendar
import datetime
import requests
import json
import sys


DATAGREPPER = 'https://apps.fedoraproject.org/datagrepper/raw'

def query(start, end, **kwargs):
    messages = []
    cnt = 1
    while True:
        params = {
            'start': calendar.timegm(start.timetuple()),
            'end': calendar.timegm(end.timetuple()),
            'rows_per_page': 100,
            'page': cnt,
        }

        # Merge in our argued filters
        params.update(kwargs)

        req = requests.get(DATAGREPPER, params=params)
        json_out = json.loads(req.text)

        info = '{0} - page: {1}/{2}\r'.format(
            kwargs, cnt, json_out['pages'])
        sys.stdout.write(info)
        sys.stdout.flush()

        messages.extend(json_out['raw_messages'])

        cnt += 1
        if cnt > int(json_out['pages']):
            break

    return messages

if __name__ == '__main__':
    results = query(
        start=datetime.datetime.now() - datetime.timedelta(days=0.1),
        end=datetime.datetime.now(),
        categories=['fedoratagger']
    )
    print len(results), 'results found.'
