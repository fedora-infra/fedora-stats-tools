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

curr=time.time()
with open('TimeStampedMonthwise.txt', 'w+') as f:
    print "---------------------------------------"
    print "MONTHWISE STATISTICS"
    for query in queries:
        print "---------------------------------------"
        print "query is", query
        print "---------------"
	f.write('query is '+str(query)+"\n")
        for month in range(12):
            end = curr - one_month * month
            start = curr - one_month * (month + 1)
            ctr=get_count(start, end, query)
	    print str(time.ctime(int(start)))+" "+str(time.ctime(int(end)))+" "+str(ctr)
	    f.write(str(time.ctime(int(start)))+" "+str(time.ctime(int(end)))+" "+str(ctr)+"\n")
	f.write("\n\n")       	
	print
        print "---------------------------------------"


with open('TimeStampedWeekwise.txt', 'w+') as f :
    print "---------------------------------------"
    print "WEEKWISE STATISTICS"
    for query in queries:
        print "---------------------------------------"
        print "query is", query
        print "---------------"
        f.write("query is "+str(query)+"\n")
        for week in range(52):
            end = curr - one_week * week
            start = curr - one_week * (week + 1)
            ctr=get_count(start, end, query)
	    print str(time.ctime(int(start)))+" "+str(time.ctime(int(end)))+" "+str(ctr)
	    f.write(str(time.ctime(int(start)))+" "+str(time.ctime(int(end)))+" "+str(ctr)+"\n")
        f.write("\n\n")
        print
        print "---------------------------------------"

with open("TimeStampedDaywise.txt",'w+') as f :
    print "---------------------------------------"
    print "DAYWISE STATISTICS"
    for query in queries:
        print "---------------------------------------"
        print "query is", query
        f.write("query is "+str(query)+"\n")
        print "---------------"
        for day in range(365):
            end = curr - one_day * day
            start = curr - one_day * (day + 1)
            ctr=get_count(start, end, query)
	    print str(time.ctime(int(start)))+" "+str(time.ctime(int(end)))+" "+str(ctr)
	    f.write(str(time.ctime(int(start)))+" "+str(time.ctime(int(end)))+" "+str(ctr)+"\n")
        f.write("\n\n")     
        print
        print "---------------------------------------"


