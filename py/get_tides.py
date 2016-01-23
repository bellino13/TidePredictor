import pandas
from urllib.parse import quote
from urllib.request import urlopen
from urllib.error import URLError
from datetime import datetime, timedelta


def get_api_response(url):
    try:
        res = urlopen(url)
        return res.read()

    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)


station = '8726520' # St Petersburg
host = r'http://tidesandcurrents.noaa.gov'
api_string = r'/api/datagetter?'

now = datetime.now()
now_date = '{0}{1:0>2d}{2:0>2d} {3:0>2d}:{4:0>2d}'.format(now.year, now.month, now.day, now.hour, now.minute)
begin = now-timedelta(hours=6)
begin_date = '{0}{1:0>2d}{2:0>2d} {3:0>2d}:{4:0>2d}'.format(begin.year, begin.month, begin.day, begin.hour, begin.minute)
end = now+timedelta(hours=18)
end_date = '{0}{1:0>2d}{2:0>2d} {3:0>2d}:{4:0>2d}'.format(end.year, end.month, end.day, end.hour, end.minute)

# Grab water levels
options = ['range={}'.format(6),    # Get the last 6 hours of data
           'station={}'.format(station),
           'product=water_level',
           'datum=mllw',
           'units=english',
           'time_zone=lst_ldt',
           'application=web_services',
           'format=xml']
fetch_url = host + api_string + '&'.join(options)
url = quote(fetch_url, safe="%/:=&?~#+!$,;'@()*[]")
water_levels = get_api_response(url)
print('water levels')
print(water_levels)

# Grab tide predictions
options = ['begin_date={}'.format(now_date),
           'end_date={}'.format(end_date),
           'station={}'.format(station),
           'product=predictions',
           'datum=mllw',
           'units=english',
           'time_zone=lst_ldt',
           'application=web_services',
           'format=xml']
fetch_url = host + api_string + '&'.join(options)
url = quote(fetch_url, safe="%/:=&?~#+!$,;'@()*[]")
tides = get_api_response(url)
print('tides')
print(tides)

t_offset_high = -17   # add minutes
t_offset_low = -17    # add minutes
h_offset_high = 0.66  # multiplier
h_offset_low = 0.82   # multiply low tide

'''
https://tidesandcurrents.noaa.gov/noaatidepredictions/serveimage?filename=images/8725747/21012016/998/8725747_2016-01-22.gif
Status API Training Shop Blog About Pricing
'''
