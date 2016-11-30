import requests
import csv
import time
from datetime import date
from dateutil.rrule import rrule, DAILY

with open('april_wu1.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['hour', 'day', 'month', 'year', 'precipitation_in', 'temp_f', 'temp_c', 'humidity'])
    
    urlstart = 'http://api.wunderground.com/api/[API_KEY]/history_'
    urlend = '/q/NY/New_York.json'
    
    st = date(2015, 4, 1)
    end = date(2015, 4, 30)
    
    for dt in rrule(DAILY, dtstart=st, until=end):
        d = requests.get(urlstart + str(dt.strftime("%Y%m%d")) + urlend).json()
        try:
            for h in d['history']['observations']:
                writer.writerow([h['date']['hour'], h['date']['mday'], h['date']['mon'], h['date']['year'],
                                 h['precipm'], h['tempi'], h['tempm'], h['hum']])
        except KeyError:
            time.sleep(600)
            d = requests.get(urlstart + str(dt.strftime("%Y%m%d")) + urlend).json()
            for h in d['history']['observations']:
                writer.writerow([h['date']['hour'], h['date']['mday'], h['date']['mon'], h['date']['year'],
                                 h['precipm'], h['tempi'], h['tempm'], h['hum']])