from __future__ import print_function
import pandas as pd
import matplotlib.pyplot as plt
from urllib2 import URLError, quote, urlopen
from datetime import datetime, timedelta
from lxml import etree


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


def parse_api_response(xml, tag):
    data = list()
    root = etree.fromstring(xml)
    for child in root:
        for element in child.findall("tag={}".format(tag)):
            data.append((element.attrib['t'], element.attrib['v']))

    df = pd.DataFrame(data, columns=['date', 'value'])
    df.date = pd.to_datetime(df.date)
    df.value = pd.to_numeric(df.value)
    df = df.set_index(['date'])
    s = df.value
    return s




station = '8726520'  # St Petersburg
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
xml = get_api_response(url)
print(xml)
wl = parse_api_response(xml, 'wl')
# print(wl)


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
xml = get_api_response(url)
print(xml)
pr = parse_api_response(xml, 'pr')


'''
https://tidesandcurrents.noaa.gov/noaatidepredictions/serveimage?filename=images/8725747/21012016/998/8725747_2016-01-22.gif
'''
