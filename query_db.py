__author__ = 'judith'

#import the required modules
import os.path
import gzip
import urllib2
import json
from Bio.Seq import Seq
from access_p3p_selenium import scrap_p3p

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

# from the filename obtained from fetch_db_name result fetch the corresponding data for the id
def fetch_circ_data(filename, id):
    data = json.load(open(filename))
    return data[id][0]

# function obtains the backsplice sequence
def get_circ_sequence(assembly, circ_data, offset=200):
# if its positive strand the offset is subtracted from end and add to the start sequence
    if circ_data['strand'] == "+":
        start1 = int(circ_data['end']) - offset
        end1 = int(circ_data['end'])
        start2 = int(circ_data['start'])
        end2 = int(circ_data['start']) + offset
        seq1 = get_seq_from_das(assembly, circ_data['chrom'], start1, end1)
        seq2 = get_seq_from_das(assembly, circ_data['chrom'], start2, end2)
# if its negative strand, reverse complement of the obtained sequence is joined together
    elif circ_data['strand'] == "-":
        start1 = int(circ_data['start'])
        end1 = int(circ_data['start']) + offset
        start2 = int(circ_data['end']) - offset
        end2 = int(circ_data['end'])
        seq1_rc = get_seq_from_das(assembly, circ_data['chrom'], start1, end1)
        seq2_rc = get_seq_from_das(assembly, circ_data['chrom'], start2, end2)
        seq1 = str(Seq(seq1_rc).reverse_complement())
        seq2_rc = get_seq_from_das(assembly, circ_data['chrom'], start2, end2)
        seq2 = str(Seq(seq2_rc).reverse_complement())
# returns the sum of seq1 and seq2 from start and end site based on the offset
    return seq1+seq2


def get_seq_from_das(assembly, chromosome, start, end):
    coordinates = "%s:%s,%s" % (chromosome, start, end)
    das_url = "http://genome.ucsc.edu/cgi-bin/das/" + assembly + "/dna?segment=" + coordinates
    usock = urllib2.urlopen(das_url)
    das_data = usock.read()
    usock.close()
    seq_start_flag = False
    sequence = ""
    for line in das_data.split("\n"):
        if line.find("</DNA>") != -1:
            break
        if seq_start_flag:
            sequence += line
        if line.find("DNA length=") != -1:
            seq_start_flag = True
    return sequence


def fetch_annotation(circ_data):
    rf = os.path.join(datadir, 'refFlat.txt')
    if os.path.isfile(rf) is False:
        get_refflat()
    result = []
    with open(rf) as handle:
        for line in handle:
            cols = line.rstrip('\n').split('\t')
            if cols[2] == circ_data['chrom']:
                cs = int(circ_data['start'])
                ce = int(circ_data['end'])
                gs = int(cols[4])
                ge = int(cols[5])
                if cs > gs and ce < ge:
                    result.append(cols)
                elif cs > gs and cs < ge:
                    result.append(cols)
                elif ce < ge and ce > gs:
                    result.append(cols)
    return result


def get_refflat():
    refflat_link = 'http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refFlat.txt.gz'
    response = urllib2.urlopen(refflat_link).read()
    gz_rf = os.path.join(datadir, 'refFlat.txt.gz')
    rf = os.path.join(datadir, 'refFlat.txt')
    with open(gz_rf, 'wb') as out:
        out.write(response)

    with gzip.open(gz_rf, 'rb') as infile:
        with open(rf, 'w') as outfile:
            for line in infile:
                outfile.write(line)


if __name__ == '__main__':
    circid = raw_input("Please Enter circular RNA ID: ")
    circ_data = fetch_circ_data(fetch_db_name('Homo sapiens', 'all'), circid)
    offset = int(raw_input("Please Enter the offset for Primer: "))
    raw_anno = fetch_annotation(circ_data)
    cs = int(circ_data['start'])
    ce = int(circ_data['end'])
    #print circ_data
    print "\n\nCircular RNA ID: " + str(circid)
    print "Circular RNA co-ordinates: " + str(cs)+ "-" + str(ce)
    print "\n Gene and Transcripts covered by the circular RNA \n"
    for anno in raw_anno:
        print "Gene Name: " + anno[0] + " Transcript ID: " + anno[1]
        ex_starts = [int(c) for c in anno[9].split(',')[:-1]]
        ex_ends = [int(c) for c in anno[10].split(',')[:-1]]
        for i, j in zip(ex_starts, ex_ends):
            #print i, j, j-i,
            if anno[3] == "+":
                dist = i - int(anno[4])
            elif anno[3] == '-':
                dist = int(anno[5]) - j
            #print dist,
            """if cs >= i and ce <= j:
                print 'Yes'
            elif cs >= i and cs <= j:
                print 'Yes'
            elif ce <= j and ce >= i:
                print 'Yes'
            else:
                print 'No'"""
    sequence = get_circ_sequence('hg19', circ_data, offset)
    target = "%d,%d" % (offset, 10)
    print "\nPrimer sequence: "
    print scrap_p3p(sequence, target)


