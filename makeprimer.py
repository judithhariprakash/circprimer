

"""def joining_seq(dict1,dict2):
    OUT = open('out.txt','w')
    final_template = {}
    for n, every in enumerate(dict1):
        strand = dict1[every][0]
        if every in dict2:
            if strand == '+':
                final_template[every] = dict1[every][1]+dict2[every][1]
            if strand == '-':
                final_template[every] = dict2[every][1]+dict1[every][1]
    OUT.write(str(final_template))"""

if __name__ == '__main__':
    file = open('hg19_templateseq.txt','r')
    check = ">"
    circid = ""
    seq1_dict = {}
    seq2_dict = {}
    for n,line in enumerate(file):
        if check in line:
            cols = line.rstrip('\n').split('_')
            print circid,
            part = cols[7]
            partno = part.split(' ')
            pno = partno[0]
            circid = cols[4]+ "_" + cols[5]+ "_" +cols[6]
            strands = partno[-2]
            std = strands.split('=')
            strand = std[1]
            print strand
            if pno == '1':
                seq1_dict[circid] = (strand,(file.next()).rstrip('\n'))
            if pno == '2':
                seq2_dict[circid] = (strand,(file.next()).rstrip('\n'))
    #joining_seq(seq1_dict,seq2_dict)