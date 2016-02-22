#Script to understand User activity after an event
#Imports user list from Badge Awarded for event or else from fedmsg activity i.e. signed in to Fedora Badges for first time
#Returns user activity : pre event, during event, post event and list of new contributors onboarded

import re
import copy
import time
import requests
import urllib2



# <---------EDIT EVENT DETAILS HERE ------------>
BADGE_URL =  "https://badges.fedoraproject.org/badge/fosdem-2016-attendee"
EVENT_START = '2016-01-30 00:00:00' #'YYYY-MM-DD HH:MM:SS' 
EVENT_END = '2016-02-01 00:00:00' #'YYYY-MM-DD HH:MM:SS'
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
    response = requests.get(badge_url)
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
    init="<b>fedbadges.person.login.first</b></a></p>"
    end=" logged in to badges.fedoraproject.org for the first time " 
    sindex = [m.start() for m in re.finditer(init, text)]
    eindex = [m.start() for m in re.finditer(end , text)]
    if len(sindex)!= len(eindex) :
       print "BIG PROBLEM"
    userList = []
    for i in range(len(sindex)) :
        userList.append(str(text[sindex[i]+len(init)+12:eindex[i]].strip("\n\t ")))
    return userList

def get_user_activity(username , start_time , end_time , time_delta ) :
    prevMsgs=get_count(username , start_time - time_delta , time_delta)
    EventMsgs=get_count(username , start_time , end_time - start_time )
    afterMsgs=get_count(username , end_time , time_delta )
    print str(username)+", "+str(prevMsgs)+", "+str(EventMsgs)+", "+str(afterMsgs)

def new_user(username , end_time) :
    end_time = end_time - 86400
    url = "https://apps.fedoraproject.org/datagrepper/raw?user="+str(username)+"&order=asc"
    response = requests.get(url)
    data = response.json()
    if data['raw_messages'][0]['timestamp'] > end_time  :
        return True
    return False    






curr = time.time()
start_time =   int(time.mktime(time.strptime( EVENT_START, '%Y-%m-%d %H:%M:%S')))
end_time = int(time.mktime(time.strptime( EVENT_END , '%Y-%m-%d %H:%M:%S'))) 
userList = get_users_from_badge(BADGE_URL) # for getting Users from Fedora Badges
#userList = get_users_from_datagrepper(get_datagrepper_url(start_time,end_time)) # for getting Users from Datagrepper messages

print "<---------------------- NEW FEDORA CONTRIBUTORS AFTER THE EVENT -----------------------------------------> "
ctr = 0
for username in userList :
    if new_user(username , start_time) :
        ctr = ctr + 1 
        print ctr , username   

print "Total Fedora Contributors in Event : "+str(len(userList))
print " New Fedora Contributors Onboarded in Event : "+str(ctr)

print "<--------------------------------------------------------------------------------------------------------->"        


print "<------------ SHORT TERM ACTIVITY DETAILS ------------------------->\n"
time_delta = one_day*20
for username in userList :
    get_user_activity(username , start_time , end_time , time_delta )
print "<------------------------------------------------------------------>\n\n"   
    


print "<------------ LONG TERM ACTIVITY DETAILS ------------------------->\n"
time_delta = curr - end_time
if time_delta > one_year :
    time_delta = one_year
for username in userList :
    get_user_activity(username , start_time , end_time , time_delta )
print "<------------------------------------------------------------------>\n\n"   

    