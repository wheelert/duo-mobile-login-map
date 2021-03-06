#!/usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import
import csv
import sys
import duo_client
import json
from six.moves import input
import time 
import os
import os.path

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="duo login app", timeout=None)

# Configuration and information about objects to create.
admin_api = duo_client.Admin(
    ikey='CHANGEME',
    skey='CHANGEME',
    host='api-xxxxx.duosecurity.com',
)



_today = datetime.today()
td = timedelta(30)
_date2 = _today - td

_mintime = _date2.timestamp()

# Retrieve log info from API:
logs = admin_api.get_authentication_log(mintime=_mintime)


# Count authentications by country:
counts = dict()
sites = []


for log in logs:
    city = log['location']['city']
    state = log['location']['state']
    country = log['location']['country']
    
    _timestamp = date.fromtimestamp( int(log['timestamp']) )
    
    if city != '':
    	_loc = log['location']['city'] +' '+ log['location']['state'] + ',' + log['location']['country']
    	if _loc not in sites:
    		sites.append([_loc,log])


_coords = []
_string = ""

_cnt = 1

for _site in sites:
	_data = geolocator.geocode(_site[0]).raw
	_coords.append([_data['lon'],_data['lat']])
	log = _site[1]
	
	if log['result'] == "SUCCESS":
		_string += "var marker"+str(_cnt)+" = L.marker(["+ _data['lat'] +","+ _data['lon'] +"]).addTo(map)\n"
	else:	
		_string += "var marker"+str(_cnt)+" = L.marker(["+ _data['lat'] +","+ _data['lon'] +"],{color: 'red'}).addTo(map)\n"
		
	_datetime = datetime.fromtimestamp( int(log['timestamp']) )
	_strtime = str(_datetime.month)+"/"+str(_datetime.day)+"/"+str(_datetime.year)+" "+str(_datetime.hour)+":"+str(_datetime.minute)+":"+str(_datetime.second)	
		
	_poptxt = " <b>"+str(log['email'])+"</b><br> <b>App:</b>"+str(log['integration'])+"<br> <b>IP:</b>"+str(log['ip'])+"<br /><b>Location:</b> "+log['location']['city']+","+log['location']['state']+"<br /><b>date:</b>"+_strtime
		
	_string += "marker"+str(_cnt)+".bindPopup('"+ _poptxt +"').openPopup();\n"
	
	time.sleep(2)
	_cnt +=1
	
	
print(_string)


map_file = open("map_template.html", "r")
html_data = map_file.read()
map_file.close()

map_data = html_data.replace('##MARKERS##',_string)

if os.path.exists("map.html"):
	os.remove("map.html")

f = open("map.html","a")
f.write(map_data)
f.close()


