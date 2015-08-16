__author__ = 'judith'

import urllib2
from bs4 import BeautifulSoup
import json

response = urllib2.urlopen('http://www.circbase.org/cgi-bin/downloads.cgi')
html = response.read()
soup = BeautifulSoup(html, "html.parser")
start = False
data = {}
for i in soup.find_all('tr'):
    if start is False:
        if i['class'][0] == u'title':
            for j in i.find_all('td'):
                if j.contents[0] == u'circRNAs':
                    start = True
    else:
        if i['class'][0] == u'strong':
            for j in i.find_all('td'):
                organism = str(j.contents[0]).lstrip('<i>').rstrip('</i>')
                data[organism] = {'all': {}}
                break
            for j in i.find_all('a'):
                data[organism]['all'][str(j.contents[0]).lstrip('.')] = 'http://www.circbase.org' + str(j['href'])[2:]
        elif i['class'][0] == u'medium':
            for j in i.find_all('td'):
                study = str(j.contents[0]).lstrip('<td>').rstrip('</td>')
                data[organism][study] = {'all': {}}
                break
            for j in i.find_all('a'):
                data[organism][study]['all'][str(j['href'])[2:].split('.')[1]] = \
                    'http://www.circbase.org' + str(j['href'])[2:]
        elif i['class'][0] == u'low':
            for j in i.find_all('td'):
                sample = str(j.contents[0]).lstrip('<td>').rstrip('</td>')
                data[organism][study][sample] = {}
                break
            for j in i.find_all('a'):
                data[organism][study][sample][str(j['href'])[2:].split('.')[1]] = \
                    'http://www.circbase.org' + str(j['href'])[2:]

with open('circ_base_links.json', 'w') as out:
    json.dump(data, out, indent=2)
