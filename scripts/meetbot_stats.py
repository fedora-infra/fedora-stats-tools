import copy
import time

import requests

one_minute = 60
one_hour = one_minute * 60
one_day = one_hour * 24
one_week = one_day * 7
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
        'topic': 'org.fedoraproject.prod.meetbot.meeting.complete',
    },
    {
        'topic': 'org.fedoraproject.prod.meetbot.meeting.item.help' ,
    },
    {
        'topic': 'org.fedoraproject.prod.meetbot.meeting.item.link' ,
    },
    {
        'topic': 'org.fedoraproject.prod.meetbot.meeting.start',
    },
    {
        'topic' : 'org.fedoraproject.prod.meetbot.meeting.topic.update',
    },
    
]

with open("monthwise.txt",'w+') as f :
	for query in queries:
		print "---------------------------------------"
		print "MONTHWISE STATISTICS"
		print "---------------------------------------"
		print "query is", query
		print "---------------"
		f.write("query is "+str(query)+"\n")
		for month in range(12):
			end = time.time() - one_month * month
			start = time.time() - one_month * (month + 1)
			print "%i months ago" % month,
			ctr=get_count(start, end, query)
			print str(ctr)
			f.write(str(month)+" months ago "+str(ctr)+"\n")
		f.write("\n\n")
		print
		print "---------------------------------------"

with open("weekwise.txt",'w+') as f :
	for query in queries:
		print "---------------------------------------"
		print "WEEKWISE STATISTICS"
		print "---------------------------------------"
		print "query is", query
		print "---------------"
		f.write("query is "+str(query)+"\n")
		for week in range(52):
			end = time.time() - one_week * week
			start = time.time() - one_week * (week + 1)
			print "%i weeks ago" % week,
			ctr=get_count(start, end, query)
			print str(ctr)
			f.write(str(week)+" weeks ago "+str(ctr)+"\n")
		f.write("\n\n")
		print
		print "---------------------------------------"

with open("daywise.txt",'w+') as f :
	for query in queries:
		print "---------------------------------------"
		print "DAYWISE STATISTICS"
		print "---------------------------------------"
		print "query is", query
		f.write("query is "+str(query)+"\n")
		print "---------------"
		for day in range(365):
			end = time.time() - one_day * day
			start = time.time() - one_day * (day + 1)
			print "%i days ago" % day,
			ctr=get_count(start, end, query)
			print str(ctr)
			f.write(str(day)+" days ago "+str(ctr)+"\n")
		f.write("\n\n")		
		print
		print "---------------------------------------"

