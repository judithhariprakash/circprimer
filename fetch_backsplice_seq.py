#from Bio.Seq import Seq
import urllib2

def get_seq_from_das(chromosome, start, end):
    coordinates = "%s:%s,%s" % (chromosome, start, end)
    das_url = "http://genome.ucsc.edu/cgi-bin/das/hg19" + "/dna?segment=" + coordinates
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

if __name__ == '__main__':
    file =  open ('hg19_all_templates.bed', 'r')
    template = {}
    for n, line in enumerate(file):
        print n,
        cols = line.rstrip('\n').split('\t')
        chrom = cols[0]
        start = cols[1]
        end = cols[2]
        circ_id = cols[3]
        seq = get_seq_from_das(chrom, start, end)
        template[circ_id] = seq
        print template
        break
    print len(template)