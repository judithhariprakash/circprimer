from Bio.Seq import Seq
import urllib2

#fetches the sequence from ucsc file based on the chromosome co-ordinates
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

def rev_comp(seq_part, strand):
    if strand == '+':
        #print "\n Sequence un altered\n"
        return seq_part
    elif strand == '-':
        #print "\nReverse Compliment\n"
        return str(Seq(seq_part).reverse_complement())

def join_seq(circ_id, seq_rc, strand):
    #temp = {}
    seq = ""
    cid = ""
    for line in circ_id:
        cols = circ_id.split('_')
# how to access the second line of the bed file to compare the cid to join the sequence
        cid = cols[0]+ "_" + cols[1]+ "_" +cols[2]
        if cols[3] == '1':
            seq = seq_rc
            print cid, seq
            break
        elif cols[3] == '2':
            pass

if __name__ == '__main__':
    file =  open ('hg19_all_templates.bed', 'r')
    template = {}
# Opens the bed file of backsplice, assigns the co-ordinates and calls the das assembly function to obtain the sequence
    for n, line in enumerate(file):
        #print n,
        cols = line.rstrip('\n').split('\t')
        chrom = cols[0]
        start = cols[1]
        end = cols[2]
        circ_id = cols[3]
        strand = cols[5]
        seq_part = get_seq_from_das(chrom, start, end)
        seq_rc = rev_comp(seq_part, strand)
        join_seq(circ_id,seq_rc, strand)
        break