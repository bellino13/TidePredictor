#!/usr/bin python2
from urllib import urlopen


def index(req):
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
