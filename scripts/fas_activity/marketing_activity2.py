#!/usr/bin/env python -tt
#-*- coding: utf-8 -*-

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
This program retrieves all the people in the Marketing group use FAS and
datagrepper to figure out the last time they have been active in the Fedora
infrastructure at large.

Dependencies:
* python-requests
* python-argparse
* python-fedora
* python-arrow
* python-progressbar
"""

import datetime
import getpass
import json
import time
import urllib
import socket

import arrow
import fedora.client.fas2
import requests

from progressbar import Bar, ETA, Percentage, ProgressBar, RotatingMarker


DATAGREPPER_URL = 'https://apps.fedoraproject.org/datagrepper/raw/'


def get_fas_userlist(fas_credentials):
    creds = fas_credentials

    fasclient = fedora.client.fas2.AccountSystem(
        username=creds['username'],
        password=creds['password'],
    )

    timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(600)
    try:
        print("Downloading FAS cache - be patient")
        request = fasclient.send_request(
            '/user/list',
            req_params={'search': '*'},
            auth=True)
    finally:
        socket.setdefaulttimeout(timeout)

    # We don't actually check for CLA+1, just "2 groups"
    output = []
    for people in request['people']:
        if 'group_roles' in people and \
                'marketing' in people['group_roles'] and \
                people['group_roles'][
                    'marketing']['role_status'] == 'approved':
            output.append(
                [people['username'], arrow.get(people['last_seen'])]
            )

    return output


def get_last_action_of_user(username):
    """ Query datagrepper to retrieve the last action of the provided user.
    """
    #print('Query history for {0}'.format(username))

    data = {
        'user': [username],
        'rows_per_page': 1,
        'order': 'desc',
    }
    output = requests.get(DATAGREPPER_URL, params=data)
    try:
        json_output = json.loads(output.text)
    except Exception, err:
        print 'ERROR for user %s' % username
        print 'ERROR:', err.message
        return []

    if not json_output['raw_messages']:
        #print 'ERROR no messages for user %s' % username
        return None

    return arrow.get(json_output['raw_messages'][0]['timestamp'])


def main():
    # We need some credential to work:
    username = raw_input('FAS username: ')
    password = getpass.getpass('FAS password: ')
    creds = { 'username': username, 'password': password}

    # Do a long query against FAS to get all the user
    peoples = get_fas_userlist(creds)
    print '%s marketing contributors to investigate' % len(peoples)
    if not peoples:
        return

    output = {}
    no_msg = []
    widgets = ['Getting date: ', Percentage(), ' ',
               Bar(marker=RotatingMarker()), ' ', ETA()]
    pbar = ProgressBar(widgets=widgets, maxval=len(peoples)).start()
    cnt = 0
    pkger_active = {}
    for row in peoples:
        people, login_date = row
        #print people, login_date
        action_date = get_last_action_of_user(people)
        if not action_date or login_date > action_date:
            action_date = login_date
        pkger_active[people] = action_date
        if action_date is not None:
            #print '  --> ', arrow.utcnow(), action_date
            delta = arrow.utcnow() - action_date
            if delta.days in output:
                output[delta.days] += 1
            else:
                output[delta.days] = 1
        else:
            no_msg.append(people)
            if 'nodate' in output:
                output['nodate'] += 1
            else:
                output['nodate'] = 1
        cnt = cnt + 1
        pbar.update(cnt)
    pbar.finish()

    with open('marketing_active_date2.csv', 'w') as stream:
        stream.write('Packager,Last activity,Last activity in days\n')
        for pkg in pkger_active:
            delta = 15552000.0
            if pkger_active[pkg] is not None:
                delta = arrow.utcnow() - pkger_active[pkg]
                delta = delta.days
            stream.write('%s,%s,%s\n' %(pkg, pkger_active[pkg], delta))
    print 'marketing_active_date2.csv written'

    with open('marketing_active_per_day2.csv', 'w') as stream:
        stream.write('Days,Numbers\n')
        days = sorted(output.keys())
        for key in days:
            stream.write('{0},{1}\n'.format(key, output[key]))
    print 'marketing_active_per_day2.csv written'

    print 'Could not find any dates for %s users' % len(no_msg)


if __name__ == '__main__':
    main()
