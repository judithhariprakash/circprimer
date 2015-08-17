__author__ = 'judith'

import urllib2
import json
import os.path

json_file = 'circ_base_links.json'
if os.path.isfile(json_file) is True:
    data = json.load(open(json_file))
else:
    print "%s not found. Existing!" % json_file
    exit()

datadir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

def fetch_data(organism, study='all', sample='all', fileformat='bed'):
    if study == 'all':
        sample = fileformat
    if organism in data:
        if study in data[organism]:
            if sample in data[organism][study]:
                link = None
                if study == 'all':
                    link = data[organism][study][sample]
                elif fileformat in data[organism][study][sample]:
                    link = data[organism][study][sample][fileformat]
                else:
                    print "Only following file formats are available:\n%s" % (
                                                          "\n".join(data[organism][study][sample].keys()))
                if link is not None:
                    filename = os.path.join(datadir, link.split('/')[-1])
                    if os.path.isfile(filename) is True:
                        print "File named '%s' already exists in '%s'. Will not download!" % (link.split('/')[-1],
                                                                                          datadir)
                    else:
                        print "Downloading file %s" % link.split('/')[-1]
                        req = urllib2.Request(link, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/14.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
                        con = urllib2.urlopen(req)
                        response = con.read()
                        if not os.path.exists(datadir):
                            os.makedirs(datadir)
                        with open(filename, 'w') as out:
                            out.write(response)
            else:
                print "Only following samples are available for %s in %s: \n%s" % (organism, study,
                                                                  "\n".join(data[organism][study].keys()))
        else:
            print "Only following studies are available for %s: \n%s" % (organism,
                                                                         "\n".join(data[organism].keys()))
    else:
        print "Only following organisms are available: \n%s" % "\n".join(data.keys())

if __name__ == '__main__':
    fetch_data('Homo sapiens')
