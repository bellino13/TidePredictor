from __future__ import print_function
import pandas as pd
import numpy as np
from urllib2 import URLError, quote, urlopen
from datetime import datetime, timedelta
from xml.etree.ElementTree import ElementTree, fromstring
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateFormatter, DateFormatter, AutoDateLocator, MinuteLocator, HourLocator, DayLocator
plt.style.use('ggplot')


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
    tree = fromstring(xml)
    if tag == 'wl':
        data = tree.findall('observations/wl')
    elif tag == 'pr':
        data = tree.findall('pr')
    values = list()
    for element in data:
        values.append((element.attrib['t'], element.attrib['v']))

    df = pd.DataFrame(values, columns=['date', 'value'])
    df.date = pd.to_datetime(df.date)
    df.value = pd.to_numeric(df.value)
    df = df.set_index(['date'])
    s = df.value
    return s


def plot(s, filename, heading=None):

    fig, ax = plt.subplots(figsize=(8, 4))

    # plot the column
    dates = s.index
    ax.plot_date(x=dates, y=s, fmt='-', color='blue',
        tz=None, xdate=True, ydate=False, linewidth=1.5)

    ax.set_ylim([s.min()-.2, s.max()+.2])

    # format the x tick marks
    # ax.xaxis.set_major_formatter(AutoDateFormatter('%M:%S'))
    # ax.xaxis.set_minor_formatter(AutoDateFormatter('%M:%S'))
    # ax.xaxis.set_major_locator(AutoDateLocator())
    # ax.xaxis.set_minor_locator(AutoDateLocator())

    # grid, legend and yLabel
    ax.grid(False)
    ax.set_ylabel('Height above MLLW')

    # heading
    if heading:
        fig.suptitle(heading, fontsize=12)
    fig.tight_layout(pad=1.5)


    # save to file
    # fig.savefig(filename, dpi=125)
    plt.show()
    plt.close()


station = '8726520'  # St Petersburg
api_base = r'http://tidesandcurrents.noaa.gov/api/datagetter?'
t_offset = -17
h_offset_high = 0.66
h_offset_low = 0.82

# Grab water levels
options = ['range={}'.format(6),    # Get the last 6 hours of data
           'station={}'.format(station),
           'product=water_level',
           'datum=mllw',
           'units=english',
           'time_zone=lst_ldt',
           'application=web_services',
           'format=xml']
fetch_url = api_base + '&'.join(options)
url = quote(fetch_url, safe="%/:=&?~#+!$,;'@()*[]")
xml = get_api_response(url)
wl = parse_api_response(xml, 'wl')


# Grab tide predictions
now = datetime.now()
now_date = '{0}{1:0>2d}{2:0>2d} {3:0>2d}:{4:0>2d}'.format(now.year, now.month, now.day, now.hour, now.minute)
begin = now-timedelta(hours=6)
begin_date = '{0}{1:0>2d}{2:0>2d} {3:0>2d}:{4:0>2d}'.format(begin.year, begin.month, begin.day, begin.hour, begin.minute)
end = now+timedelta(hours=18)
end_date = '{0}{1:0>2d}{2:0>2d} {3:0>2d}:{4:0>2d}'.format(end.year, end.month, end.day, end.hour, end.minute)
options = ['begin_date={}'.format(now_date),
           'end_date={}'.format(end_date),
           'station={}'.format(station),
           'product=predictions',
           'datum=mllw',
           'units=english',
           'time_zone=lst_ldt',
           'application=web_services',
           'format=xml']
fetch_url = api_base + '&'.join(options)
url = quote(fetch_url, safe="%/:=&?~#+!$,;'@()*[]")
xml = get_api_response(url)
pr = parse_api_response(xml, 'pr')

s = pd.concat([wl, pr])
plot(s, 'test.png', heading=None)

# Find local minima (low tides) and maxima (high tides)
maxm = argrelextrema(pr.values, np.greater)  # (array([1, 3, 6]),)
minm = argrelextrema(pr.values, np.less)  # (array([2, 5, 7]),)
print(pr.index[maxm], pr.index[minm])
