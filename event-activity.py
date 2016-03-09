#Script to understand User activity after an event
#Imports user list from Badge Awarded for event or else from fedmsg activity i.e. signed in to Fedora Badges for first time
#Returns user activity : pre event, during event, post event and list of new contributors onboarded

import re
import copy
import time
import requests
import urllib2
import json
import csv


# <---------EDIT EVENT DETAILS HERE ------------>
TYPE_ID = 2 # For extracting users from Badges URL (1) , Datagrepper URL (2)
URL = "https://apps.fedoraproject.org/datagrepper/raw?topic=org.fedoraproject.prod.irc.karma"
#URL =  "https://badges.fedoraproject.org/badge/fosdem-2014-attendee"
EVENT_START = '2014-02-01 00:00:00' #'YYYY-MM-DD HH:MM:SS' 
EVENT_END = '2014-02-03 00:00:00' #'YYYY-MM-DD HH:MM:SS'
# <------------- EDITS END ----------------------->

one_minute = 60
one_hour = one_minute * 60
one_day = one_hour * 24
one_month = one_day * 30
one_year = one_day * 365


def get_datagrepper_url( start_time , end_time ) :
    topic = "org.fedoraproject.prod.fedbadges.person.login.first"
    url = "https://apps.fedoraproject.org/datagrepper/raw?topic="+str(topic)+"&start="+str(start_time)+"&end="+str(end_time)
    return url

def get_count(username , start_time , time_delta):
    end_time = start_time + time_delta
    url = "https://apps.fedoraproject.org/datagrepper/raw?user="+str(username)+"&start="+str(start_time)+"&end="+str(end_time)
    response = requests.get(url)
    data = response.json()
    return data['total']
    
def get_users_from_badge(badge_url) :
    req = urllib2.Request(badge_url)
    try: 
        page = urllib2.urlopen(req)
        data=page.read()
    except urllib2.HTTPError or httplib.BadStatusLine or urllib2.URLError as e:
        data=str(e.fp.read()) 
    search_string = '<h1 class="section-header">Badge Holders'
    index = data.find(search_string)
    data = data[index : len(data)]
    init="https://badges.fedoraproject.org/user/"
    sindex = [m.start() for m in re.finditer(init, data)]
    userList = []
    for i in range(len(sindex)) :
        if i == len(sindex)-1 :
            text = data[sindex[i]+len(init):]
        else :
            text = data[sindex[i]+len(init):sindex[i+1]]
        ind = text.find('\">')  
        username =  text[:ind]
        print username
        userList.append(username)
    return userList
    

def get_users_from_datagrepper(datagrepper_url) :
    userList = []
    response = requests.get(datagrepper_url)
    data = response.json()
    NUM_PAGES = int(data['pages'])
    for i in range(1,NUM_PAGES+1) :
        url = datagrepper_url+"&page="+str(i)
        response = requests.get(url)
        data = response.json()
        NUM_MSGS = int(data['count'])
        for j in range(0,NUM_MSGS) :
            try :
                username = str(data['raw_messages'][j]['msg']['agent'])
            except KeyError :
                username = str(data['raw_messages'][j]['msg']['owner'])
            if username not in userList :
                print username 
                userList.append(username)
    return userList       

def get_user_activity(username , start_time , end_time , time_delta ) :
    prevMsgs = get_count(username , start_time - time_delta , time_delta)
    EventMsgs = get_count(username , start_time , end_time - start_time )
    afterMsgs = get_count(username , end_time , time_delta )
    if prevMsgs == 0 :
        percent_diff = 100
    else :    
        percent_diff = int(afterMsgs*100)/int(prevMsgs) - 100  
    activity = [username , prevMsgs , EventMsgs , afterMsgs , percent_diff]    
    return activity

def new_user(username , end_time) :
    end_time = end_time - 86400
    url = "https://apps.fedoraproject.org/datagrepper/raw?user="+str(username)+"&order=asc&rows_per_page=1"
    response = urllib2.urlopen(url)
    data = json.load(response)
    if data['raw_messages'][0]['timestamp'] > end_time  :
        return True
    return False    

def get_users(URL ,TYPE_ID) :
    if TYPE_ID == 1 :
        userList = get_users_from_badge(URL)
    else :
        if TYPE_ID == 2 :
            userList = get_users_from_datagrepper(URL)
        else :
            print "\n TYPE_ID - ERROR : Choose (1) to extract list of attendees from Badges and 2 for Datagrepper\n " ; 
            userList = []
    return userList




curr = time.time()
start_time = int(time.mktime(time.strptime( EVENT_START, '%Y-%m-%d %H:%M:%S')))
end_time = int(time.mktime(time.strptime( EVENT_END , '%Y-%m-%d %H:%M:%S'))) 

print "<---------------------- GETTING EVENT PARTICIPANTS -----------------------------------------> "
if TYPE_ID == 2 :
    URL = URL + '&start='+str(start_time)+"&end="+str(end_time)
userList = get_users(URL , TYPE_ID) 
short_time_delta = one_day 
if curr - end_time < short_time_delta :
    short_time_delta = curr - end_time

long_time_delta = curr - end_time
if long_time_delta > one_day * 3:
    long_time_delta = one_day * 3


print "<---------------------- FINDING NEW FEDORA CONTRIBUTORS AFTER THE EVENT -----------------------------------------> "
ctr = 0
newUser = []
for username in userList :
    ctr = ctr + 1 
    if new_user(username , start_time) :
        newUser.append(username)

print "Total Fedora Contributors in Event : "+str(len(userList))
print " New Fedora Contributors Onboarded in Event : "+str(len(newUser))

with open('event_data'+str(curr)+'.csv', 'wb') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(['event' , URL])
    datawriter.writerow(['EVENT_START' , EVENT_START])
    datawriter.writerow(['EVENT_END' , EVENT_END ])
    datawriter.writerow([])
    datawriter.writerow(['Total Fedora Contributors in Event : ' , str(len(userList))])
    datawriter.writerow(['New Fedora Contributors Onboarded in Event' , str(len(newUser)) ])
    datawriter.writerow([])
    datawriter.writerow(['attendees'])
    datawriter.writerow(userList)
    datawriter.writerow([])
    datawriter.writerow(['new attendees'])
    datawriter.writerow(newUser)
    datawriter.writerow([])
  
short_activity , long_activity = [] , []
print "<------------ WORKING ON SHORT TERM ACTIVITY DETAILS ------------------------->\n"
for username in userList :
    short_activity.append(get_user_activity(username , start_time , end_time , short_time_delta ))

print "<------------ WORKING ON LONG TERM ACTIVITY DETAILS ------------------------->\n"
for username in userList :
    long_activity.append(get_user_activity(username , start_time , end_time , long_time_delta ))


with open('event_data'+str(curr)+'.csv', 'ab') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(['SHORT TERM ACTIVITY OF ATTENDEES '])
    datawriter.writerow([])
    datawriter.writerow(['username' , 'prevMsgs' , 'EventMsgs' , 'afterMsgs' , 'percent_diff' ])
    for activity in short_activity :
        datawriter.writerow(activity)
    datawriter.writerow([])
    datawriter.writerow(['LONG TERM ACTIVITY OF ATTENDEES '])
    datawriter.writerow([])
    datawriter.writerow(['username' , 'prevMsgs' , 'EventMsgs' , 'afterMsgs' , 'percent_diff' ])
    for activity in long_activity :
        datawriter.writerow(activity)
