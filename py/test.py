from django.http import HttpResponse
from urllib import urlopen
from flask import Flask
app = Flask(__name__)

@app.route('/')
def get_tide_graph(url):
    res = urlopen(url)
    html = None
    for line in res.readlines():
        if './serveimage?filename=' in line:
            html = line
            break
    html = html.replace('\t', '')
    html = html.replace('\n', '')
    html = html.replace('img src=".', 'img src="https://tidesandcurrents.noaa.gov/noaatidepredictions')
    response = HttpResponse(content_type="text/plain")
    response['tidegraph'] = html
    # response = HttpResponse(html, content_type="text/plain")
    print(response)
    return response

if __name__ == '__main__':
    app.run()