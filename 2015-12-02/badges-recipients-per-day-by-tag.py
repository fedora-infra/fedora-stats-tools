#!/usr/bin/env python

import collections
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

interesting_tags = [
    'content',
    'development',
    'community',
    'quality',
    'event',
    'misc',
]

print "## time,",
print ", ".join(interesting_tags)

users = collections.defaultdict(set)
last_bucket = None
for msg in messages:
    bucket = utils.daily_timebucket(msg['timestamp'])
    if not last_bucket:
        last_bucket = bucket
    if bucket != last_bucket:
        # Then we've switched to the next day
        print "%s," % str(last_bucket),
        print ", ".join(map(str, [len(users[tag]) for tag in interesting_tags]))
        # Reset our markers
        last_bucket = bucket
        users = collections.defaultdict(set)

    tags = utils.badge2tags(msg['msg']['badge']['badge_id'])
    for tag in tags:
        if tag not in interesting_tags:
            continue
        users[tag] = users[tag].union(fedmsg.meta.msg2usernames(msg, **config))
