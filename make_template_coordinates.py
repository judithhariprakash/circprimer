__author__ = 'judith'

#import the required modules
import os.path
import json

#setting the datadirectory

datadir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

#obtain the file name from json file based on the input
def fetch_db_name(organism, study, sample=None):
    jsondata = json.load(open('circ_base_links.json'))
    if study == 'all':
        link = jsondata[organism][study]['bed']
    else:
        link = jsondata[organism][study][sample]['bed']
    filename = os.path.join(datadir, link.split('/')[-1]).split('.')[0] + '.json'
    return filename

# function obtains the backsplice sequence
def get_circ_coordinates(assembly, circ_data, offset=200):
# if its positive strand the offset is subtracted from end and add to the start sequence
    if circ_data['strand'] == "+":
        start1 = int(circ_data['end']) - offset
        end1 = int(circ_data['end'])
        start2 = int(circ_data['start'])
        end2 = int(circ_data['start']) + offset
# if its negative strand, reverse complement of the obtained sequence is joined together
    elif circ_data['strand'] == "-":
        start1 = int(circ_data['start'])
        end1 = int(circ_data['start']) + offset
        start2 = int(circ_data['end']) - offset
        end2 = int(circ_data['end'])
    return ((start1, end1), (start2, end2))


if __name__ == '__main__':
    db_name = fetch_db_name('Homo sapiens', 'all')
    data = json.load(open(db_name))
    bed_data = []
    for n, circ_id in enumerate(data):
        print "\r %d" % n
        coordinates = get_circ_coordinates('hg19', data[circ_id][0])
        bed_line1 = [data[circ_id][0]['chrom'], str(coordinates[0][0]), str(coordinates[0][1]), circ_id+'_1', '0', data[circ_id][0]['strand']]
        bed_line2 = [data[circ_id][0]['chrom'], str(coordinates[1][0]), str(coordinates[1][1]), circ_id+'_2', '0', data[circ_id][0]['strand']]
        bed_data.append("\t".join(bed_line1))
        bed_data.append("\t".join(bed_line2))
    with open('hg19_all_templates.bed', 'w') as OUT:
        OUT.write("\n".join(bed_data))
