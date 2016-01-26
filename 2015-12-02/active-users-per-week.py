#!/usr/bin/env python

import utils

import fedmsg.meta
import fedmsg.config
config = fedmsg.config.load_config()
fedmsg.meta.make_processors(**config)

import time
import datetime
import logging
import sys
logging.basicConfig(level=logging.DEBUG)

verboten = [
    'org.fedoraproject.prod.buildsys.rpm.sign',
    'org.fedoraproject.prod.buildsys.repo.init',
    'org.fedoraproject.prod.buildsys.tag',
    'org.fedoraproject.prod.buildsys.untag',
]


for day in range(351, 364, 7):
    bucket = "2015-{0:0>3}".format(day - 7)
    terminus = "2015-{0:0>3}".format(day)
    start = int(time.mktime(datetime.datetime.strptime(bucket, "%Y-%j").timetuple()))
    end = int(time.mktime(datetime.datetime.strptime(terminus, "%Y-%j").timetuple()))

    print "Working on data/%s.csv" % bucket

    messages = utils.grep(
        rows_per_page=100,
        meta='usernames',
        start=start,
        end=end,
        order='asc',  # Start at the beginning, end at now.
        # Cut this stuff out, because its just so spammy.
        not_user='koschei',
        not_topic=verboten,
    )

    users = {}
    for i, msg in enumerate(messages):
        # sanity check
        if msg['topic'] in verboten:
            raise "hell"

        for user in msg['meta']['usernames']:
            users[user] = users.get(user, 0) + 1

        if i % 50 == 0:
            print ".",
            sys.stdout.flush()

    print " done with", bucket

    with open('data/%s.csv' % bucket, 'w') as f:
        for user in users:
            f.write('%s, %i\n' % (user, users[user]))
