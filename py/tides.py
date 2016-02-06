#!/usr/bin python2
from __future__ import print_function
from urllib2 import URLError, quote, urlopen
from datetime import datetime, timedelta
from xml.etree.ElementTree import ElementTree, fromstring
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, HourLocator, DayLocator
# plt.style.use('ggplot')



def index():
    # postData = req.form
    # url = str(postData['url'].value)

    station = '8726520'  # St Petersburg
    api_base = r'http://tidesandcurrents.noaa.gov/api/datagetter?'
    t_offset = -17
    h_offset_high = 0.66
    h_offset_low = 0.82

    # Grab tide predictions
    now = datetime.now()
    now_date = '{0}{1:0>2d}{2:0>2d} {3:0>2d}:{4:0>2d}'.format(now.year, now.month, now.day, now.hour, now.minute)
    begin = now-timedelta(hours=6)
    begin_date = '{0}{1:0>2d}{2:0>2d} {3:0>2d}:{4:0>2d}'.format(begin.year, begin.month, begin.day, begin.hour, begin.minute)
    end = now+timedelta(hours=18+48)
    end_date = '{0}{1:0>2d}{2:0>2d} {3:0>2d}:{4:0>2d}'.format(end.year, end.month, end.day, end.hour, end.minute)
    options = ['begin_date={}'.format(begin_date),
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

    # Apply time offset
    pr.index = pr.index+timedelta(minutes=t_offset)

    # Apply rough height offset equal to the mean of the high/low tide offsets
    pr = pr*np.mean([h_offset_high, h_offset_low])

    # Plot tide chart
    plot(pr, now)

    html = '<img src="js/tides/tides.png">'
    return html


def index2(req):
    postData = req.form
    url = str(postData['url'].value)
    res = urlopen(url)
    html = None
    for line in res.readlines():
        if './serveimage?filename=' in line:
            html = line
            break
    html = html.replace('\t', '')
    html = html.replace('\n', '')
    html = html.replace('img src=".', 'img src="https://tidesandcurrents.noaa.gov/noaatidepredictions')
    return html


def init_plotting():
    mpl.rcParams['figure.figsize'] = (4.25, 3)
    mpl.rcParams['font.size'] = 10
    mpl.rcParams['font.family'] = 'HelveticaNeue-Light', 'sans-serif'
    mpl.rcParams['font.weight'] = 'light'
    mpl.rcParams['text.color'] = '#aaaaaa'
    mpl.rcParams['axes.labelcolor'] = mpl.rcParams['text.color']
    mpl.rcParams['axes.labelsize'] = mpl.rcParams['font.size']
    mpl.rcParams['axes.titlesize'] = 1.5*mpl.rcParams['font.size']
    mpl.rcParams['legend.fontsize'] = mpl.rcParams['font.size']
    mpl.rcParams['xtick.labelsize'] = mpl.rcParams['font.size']
    mpl.rcParams['xtick.color'] = mpl.rcParams['text.color']
    mpl.rcParams['ytick.labelsize'] = mpl.rcParams['font.size']
    mpl.rcParams['ytick.color'] = mpl.rcParams['text.color']
    mpl.rcParams['savefig.dpi'] = 2*mpl.rcParams['savefig.dpi']
    mpl.rcParams['legend.frameon'] = False


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


def plot(s, now):

    init_plotting()
    fig, ax = plt.subplots()

    plt.rc('font', weight='bold')
    plt.rc('text', color='#aaaaaa')
    ax.set_axis_bgcolor('white')

    daysFmt = DateFormatter('%a')
    days = DayLocator()
    # plt.ylabel('Height above MLLW')
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(daysFmt)

    ax.plot_date(s.index.tolist(), [0]*len(s), '--', color='#aaaaaa')
    ax.plot_date((now, now), ax.get_ylim(), '--', color='#aaaaaa')
    ax.plot_date(s.index.tolist(), s.values.tolist(), '-', color='blue')

    plt.text(.1, .03, now.strftime("%I:%M %p").lstrip('0'), transform=ax.transAxes)

    plt.tick_params(axis='both',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    left='off',
                    top='off',
                    right='off',
                    bottom='off')

    for spine in ax.spines.itervalues():
        spine.set_visible(False)

    plt.tight_layout()
    plt.savefig('tides.png', transparent=False)
    # plt.show()
    # plt.close()


if __name__=='__main__':
    html = index()
    # print(html)

# station = '8726520'  # St Petersburg
# api_base = r'http://tidesandcurrents.noaa.gov/api/datagetter?'
# t_offset = -17
# h_offset_high = 0.66
# h_offset_low = 0.82
#
# # Grab water levels
# options = ['range={}'.format(6),    # Get the last 6 hours of data
#            'station={}'.format(station),
#            'product=water_level',
#            'datum=mllw',
#            'units=english',
#            'time_zone=lst_ldt',
#            'application=web_services',
#            'format=xml']
# fetch_url = api_base + '&'.join(options)
# url = quote(fetch_url, safe="%/:=&?~#+!$,;'@()*[]")
# xml = get_api_response(url)
# wl = parse_api_response(xml, 'wl')
