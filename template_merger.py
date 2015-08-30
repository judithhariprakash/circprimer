import json

def fasta_reader(filename):
    from Bio.SeqIO.FastaIO import FastaIterator
    with open(filename) as handle:
        for record in FastaIterator(handle):
            yield record


def parse_fasta_header(header):
    cols = header.split('_')
    circid = cols[4]+ "_" + cols[5]+ "_" +cols[6]
    info = cols[7].split(' ')
    id_part = info[0]
    try:
        strand = info[4].split('=')[1]
    except IndexError:
        print header
        return False
    return circid, id_part, strand


def join_seq(dict1, dict2):
    final_template = {}
    for circ_id in dict1:
        strand = dict1[circ_id][0]
        try:
            if strand == '+':
                final_template[circ_id] = dict1[circ_id][1]+dict2[circ_id][1]
            if strand == '-':
                final_template[circ_id] = dict2[circ_id][1]+dict1[circ_id][1]
        except KeyError:
            print "HOHO something went nasty with id %s" % circ_id
            continue
    return final_template


if __name__ == '__main__':
    seq1_dict = {}
    seq2_dict = {}
    skipped_fasta_headers = 0
    fasta_record = fasta_reader('hg19_templateseq.txt')
    for seq_record in fasta_record:
        parsed_header = parse_fasta_header(str(seq_record.description))
        if parsed_header is not False:
            circid, id_part, strand = parsed_header
        else:
            skipped_fasta_headers+=1
            continue
        print circid, id_part, strand
        if id_part == '1':
            seq1_dict[circid] = (strand, str(seq_record.seq))
        if id_part == '2':
            seq2_dict[circid] = (strand, str(seq_record.seq))
    final_template = join_seq(seq1_dict, seq2_dict)
    with open('merged_backsplice_sequences.json','w') as handle:
        json.dump(final_template, handle, indent=2)
    print "%d headers were skipped" % skipped_fasta_headers