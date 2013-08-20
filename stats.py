""" Some tools to grab stats from Fedora Infrastructure's datagrepper
and plot them.

There are some dependencies::

    $ sudo yum install python-progressbar python-pygal python-requests

:Author: Ralph Bean <rbean@redhat.com>

Pagination borrowed from thisweekinfedora by Pierre-Yves Chibon
https://github.com/pypingou/thisweekinfedora

License:  GPLv3+
"""

import argparse
import calendar
import datetime
import json
import time
import sys
import os
import webbrowser

import requests
import progressbar
import pygal


datagrepper_url = 'https://apps.fedoraproject.org/datagrepper/raw'


def _do_query(params):
    req = requests.get(datagrepper_url, params=params)
    return json.loads(req.text)


def query(start, end, full=False, **kwargs):

    params = {
        'start': calendar.timegm(start.timetuple()),
        'end': calendar.timegm(end.timetuple()),
    }
    params.update(kwargs)

    if not full:
        json_out = _do_query(params)
        result = int(json_out['total'])
        return result
    else:
        print "* Doing query from", start, "to", end
        print "  on", kwargs

        messages = []
        cnt = 0
        progress = progressbar.ProgressBar()
        progress.start()

        while True:
            params.update({
                'rows_per_page': 100,
                'page': cnt + 1,
            })

            json_out = _do_query(params)

            messages.extend(json_out['raw_messages'])

            cnt += 1
            progress.maxval = int(json_out['pages'])
            progress.update(cnt)
            if cnt >= int(json_out['pages']):
                break

        progress.finish()

        return messages


def graph(slug, category, date_format="%m/%y", open_when_done=False, **kwargs):
    with open('csvs/' + slug + '.csv', 'r') as f:
        data = [map(float, line.strip().split(',')) for line in f.readlines()]

    def format_date(timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.strftime(date_format)

    xaxis = [format_date(item[0]) for item in data]
    yaxis = [item[1] for item in data]

    line_chart = pygal.Line()
    line_chart.title = category
    line_chart.x_labels = xaxis
    line_chart.add(category, yaxis)

    outfile = 'svgs/' + slug + '.svg'
    line_chart.render_to_file(outfile)

    print "Wrote", outfile

    if open_when_done:
        webbrowser.open(os.path.abspath(outfile))


def daterange(start, stop, steps):
    """ A generator for stepping through time. """
    delta = (stop - start) / steps
    current = start
    while current + delta <= stop:
        yield current, current + delta
        current += delta


def collect_stats(steps, delta, category, slug, **kwargs):
    stop = datetime.datetime.now()
    start = stop - delta
    datepairs = list(daterange(start, stop, steps))

    outfile = 'csvs/' + slug + ".csv"

    print "Collecting stats for", outfile

    progress = progressbar.ProgressBar()

    results = [
        (time.mktime(j.timetuple()), query(i, j, category=[category]))
        for i, j in progress(datepairs)
    ]

    with open(outfile, 'w') as f:
        f.write('\n'.join([','.join(map(str, pair)) for pair in results]))

    print "Wrote", outfile


def slugify(category, steps, delta, **kwargs):
    return "%s-%i-%r" % (category, steps, delta)


def stats_exist(slug, **kwargs):
    return os.path.exists('csvs/' + slug + ".csv")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--steps', type=int, default=15,
        help='Number of discrete steps on the x-axis of the graph')
    parser.add_argument(
        '--delta-in-days', dest='delta', type=int, default=210,
        help='Number of days to look back in the history')
    parser.add_argument(
        '--category', default='fedoratagger',
        help="fedmsg message category to query")
    parser.add_argument(
        '--date-format', default='%m/%y',
        help="Datestring format for the graph.")
    parser.add_argument(
        '--open-when-done', action="store_true", default=False,
        help="Open the graph in default image viewer.")

    result = vars(parser.parse_args())
    result['delta'] = datetime.timedelta(days=result['delta'])
    result['slug'] = slugify(**result)
    return result


if __name__ == '__main__':
    options = parse_args()

    if not stats_exist(**options):
        collect_stats(**options)
    else:
        print "stats already exist for %r.  Re-using them." % options['slug']

    graph(**options)
