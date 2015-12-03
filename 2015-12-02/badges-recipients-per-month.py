#!/usr/bin/env python

import utils

import fedmsg.meta
import fedmsg.config
config = fedmsg.config.load_config()
fedmsg.meta.make_processors(**config)

import logging
logging.basicConfig(level=logging.DEBUG)

start = 1443074039  # A couple months ago

messages = utils.grep(
    topic='org.fedoraproject.prod.fedbadges.badge.award',
    rows_per_page=100,
    start=start,
    order='asc',  # Start at the beginning, end at now.
)


users = set()
last_bucket = None
for msg in messages:
    bucket = utils.monthly_timebucket(msg['timestamp'])
    if not last_bucket:
        last_bucket = bucket
    if bucket != last_bucket:
        # Then we've switched to the next month
        print ", ".join(map(str, [last_bucket, len(users)]))
        # Reset our markers
        last_bucket = bucket
        users = set()
    users = users.union(fedmsg.meta.msg2usernames(msg, **config))
    #print "#", bucket, len(users), users
