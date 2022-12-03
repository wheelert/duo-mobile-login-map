#!/usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import
import csv
import sys
import duo_client
import json
from six.moves import input
import time
from datetime import datetime, date, timedelta
import os
import os.path

from geopy.geocoders import Nominatim

#Escape location names 
def string_escape(s, encoding='latin-1'):
    return (s.encode('latin1')         # To bytes, required by 'unicode-escape'
             .decode('unicode-escape') # Perform the actual octal-escaping decode
             .encode('latin1')         # 1:1 mapping back to bytes
             .decode(encoding)).replace("'","")        # Decode original encoding



geolocator = Nominatim(user_agent="duo login app", timeout=None)

# Configuration and information about objects to create.
admin_api = duo_client.Admin(
     ikey='CHANGEME',
     skey='CHANGEME',
     host='api-xxxxx.duosecurity.com',
)

_today = datetime.today()
td = timedelta(5)
_date2 = _today - td

_mintime = _date2.timestamp()

# Retrieve log info from API:
logs = admin_api.get_authentication_log(mintime=_mintime)

# Count authentications by country:
counts = dict()
sites = []
log_count = len(logs)
print('parsing {log_count} logs ')

for log in logs:
    city = log['location']['city']
    state = log['location']['state']
    country = log['location']['country']

    _timestamp = date.fromtimestamp(int(log['timestamp']))

    if city != '':
        _loc = string_escape(log['location']['city']) + ' ' + log['location']['state'] + ',' + log['location']['country']
        if _loc not in sites:
            sites.append([_loc, log])

_coords = []
_string = ""

_cnt = 1

site_count = len(sites)
site_time = (site_count * 2) / 60
parse_now = datetime.now()
parese_time = timedelta(minutes=site_time)
parse_complete = parse_now + parese_time

print("parsing {site_count} sites estimated time of completion {parse_complete} ")

for _site in sites:
    if _site[0] is not None:
        print(_site[0])
        try:
            _data = geolocator.geocode(_site[0]).raw
            _coords.append([_data['lon'], _data['lat']])
            log = _site[1]
            log_time = datetime.fromtimestamp(log['timestamp'])
        except:
            continue
            
        if log['result'] == "SUCCESS":
            _string += "var marker" + str(_cnt) + " = L.marker([" + _data['lat'] + "," + _data['lon'] + "]).addTo(map)\n"
            if log['integration'] == "NHC Remote Desktop":
                _string += "marker" + str(_cnt) + "._icon.classList.add('marker_green');\n"
        
        else:
            _string += "var marker" + str(_cnt) + " = L.marker([" + _data['lat'] + "," + _data['lon'] + "]).addTo(map)\n"
            _string += "marker" + str(_cnt) + "._icon.classList.add('marker_red');\n"
        
        _poptxt = " <b>" + str(log['email']) + "</b><br> <b>App:</b>" + str(log['integration']) + "<br> <b>IP:</b>" + str(log['ip']) + "<br /><b>Location:</b> " + string_escape(log['location']['city']) + "," + string_escape(log['location']['state']) + "<br /><b>date:</b>" + str(log_time)
        
        _string += "marker" + str(_cnt) + ".bindPopup('" + _poptxt + "').openPopup();\n"
        
        time.sleep(2)
        _cnt += 1
        
print(_string)

map_file = open("map_template.html", "r")
html_data = map_file.read()
map_file.close()

map_data = html_data.replace('##MARKERS##', _string)

if os.path.exists("map.html"):
    os.remove("map.html")

f = open("map.html", "a")
f.write(map_data)
f.close()
