import random
import json
import os
import tempfile


def get_random_ids(data, num_ids):
	return random.sample(data.keys(), num_ids)


def run_primer3(seq_id, seq):
	params = "SEQUENCE_TARGET=180,40\nPRIMER_PRODUCT_SIZE_RANGE=100-400\n=\n"
	temp_file_data = "SEQUENCE_ID=%s\nSEQUENCE_TEMPLATE=%s\n" % (seq_id, seq) + params
	temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
	temp_file.write(temp_file_data)
	temp_file.close()
	cmd = 'primer3_bin/primer3_core -p3_settings_file=primer3_bin/circrna_primers_settings.p3 %s' % (temp_file.name)
	output = os.popen(cmd).read()
	os.system('rm %s' % temp_file.name)
	return output


if __name__ == '__main__':
	with open('merged_backsplice_sequences.json') as handle:
		data = json.load(handle)
	random_ids = get_random_ids(data, 1)
	print run_primer3(random_ids[0], data[random_ids[0]])
