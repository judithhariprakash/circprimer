import random
import json
import os
import tempfile
import sys
from multiprocessing import Pool

with open('merged_backsplice_sequences.json') as handle:
		data = json.load(handle)

def run_primer3(circ_id):
	temp_file_data = "SEQUENCE_ID=%s\nSEQUENCE_TEMPLATE=%s\n=\n" % (circ_id, data[circ_id])
	temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
	temp_file.write(temp_file_data)
	temp_file.close()
	cmd = 'primer3_bin/primer3_core -p3_settings_file=primer3_bin/circrna_primers_settings.p3 %s' % (temp_file.name)
	output = os.popen(cmd).read()
	os.system('rm %s' % temp_file.name)
	return output


def parse_primer3_output(unparsed_output):
	output_dict = {}
	for line in unparsed_output.split('\n'):
		cols = line.rstrip('\n').split('=')
		try:
			output_dict[cols[0]] = cols[1]
		except IndexError:
			pass
	num_primers =  int(output_dict['PRIMER_PAIR_NUM_RETURNED'])
	if num_primers > 0:
		parsed = {}
		for i in range(num_primers):
			parsed['primer_pair_%d' % i] = {
				"left_seq": output_dict['PRIMER_LEFT_%d_SEQUENCE' % i],
				"right_seq": output_dict['PRIMER_RIGHT_%d_SEQUENCE' % i],
				"left_gc": output_dict['PRIMER_LEFT_%d_GC_PERCENT' % i],
				"right_gc": output_dict['PRIMER_RIGHT_%d_GC_PERCENT' % i],
				"left_tm": output_dict['PRIMER_LEFT_%d_TM' % i],
				"right_tm": output_dict['PRIMER_RIGHT_%d_TM' % i],
				"left_pos": output_dict['PRIMER_LEFT_%d' % i],
				"right_pos": output_dict['PRIMER_RIGHT_%d' % i],
				"product_size": output_dict['PRIMER_PAIR_%d_PRODUCT_SIZE' % i]
			}
	else:
		return False
	return parsed

def multiprocess_wrapper(circ_id):
	unparsed_output = run_primer3(circ_id)
	parsed_output = parse_primer3_output(unparsed_output)
	return parsed_output


if __name__ == '__main__':
	result = {}
	skipped_ids = []
	pool = Pool(processes=4)
	print len(data)
	id_list = []
	for n,circ_id in enumerate(data):
		print "\r %d" % n,
		sys.stdout.flush()
		id_list.append(circ_id)
		if len(id_list) == 4:
			parsed_outputs = pool.map(multiprocess_wrapper, id_list)
			for cid, output in zip(id_list, parsed_outputs):
				if output is not False:
					result[cid] = output
				else:
					skipped_ids.append(cid)
			id_list = []
	with open('hg19_circ_primers.json', 'w') as outfile:
		json.dump(result, outfile, indent=2)
	print "%d IDs skipped" % len(skipped_ids)
	print
	print skipped_ids


