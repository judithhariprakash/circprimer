__author__ = 'judith'

import os.path
import json

datadir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')


def create_db(filename):
    dbname = os.path.join(datadir, filename.split('.')[0] + '.json')
    if os.path.isfile(dbname) is True:
        print "Database '%s' already exists. Exiting!" % dbname
        exit()
    if os.path.isfile(os.path.join(datadir, filename)) is False:
        print "File '%s' doesn't exist. Exiting!" % filename
        exit()
    data = {}
    with open(os.path.join(datadir, filename)) as handle:
        for num, line in enumerate(handle):
            if line[0] == '#':
                continue
            else:
                cols = line.rstrip('\n').split('\t')
                if cols[3] in data:
                    data[cols[3]].append({
                        'chrom': cols[0], 'start': cols[1], 'end': cols[2], 'score': cols[4], 'strand': cols[5],
                        'thickStart': cols[6], 'thickEnd': cols[7], 'itemRgb': cols[8], 'blockCount': cols[9],
                        'blockSizes': cols[10], 'exonStarts': cols[11]
                    })
                else:
                    data[cols[3]] = [{
                        'chrom': cols[0], 'start': cols[1], 'end': cols[2], 'score': cols[4], 'strand': cols[5],
                        'thickStart': cols[6], 'thickEnd': cols[7], 'itemRgb': cols[8], 'blockCount': cols[9],
                        'blockSizes': cols[10], 'exonStarts': cols[11]
                    }]
    with open(dbname, 'w') as out:
        json.dump(data, out, indent=2)

if __name__ == '__main__':
    create_db('hsa_hg19_circRNA.bed')
