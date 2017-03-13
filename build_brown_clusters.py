# -*- coding: UTF-8 -*-
import os, sys, getopt, subprocess, gzip, json
from GZIPTweetStream import GZIPTweetStream
from text_utils import rand_str

def run_brown_clustering(input_file, c, out_dir):
	#Create temporary directories to store input/output files
	in_dir = "./input/"+rand_str(15)
	print "Creating temp directories."
	try:
		os.makedirs(in_dir)
	except Exception, e:
		print "Didnt create temp input dir (",str(e),")"

	try:
		os.makedirs(out_dir)
	except Exception, e:
		#TODO: should probably clear the directory for new files?
		print "Didnt create temp output dir (",str(e),")"


	#extract text from gzipped json file
	#write texts to temp file, tokens separated by spaces, one text per line
	print "Constructing input file."
	stream = GZIPTweetStream([input_file])
	in_fn = "inputfile"
	in_fn = in_dir+"/"+in_fn
	with open(in_fn,"w+") as f:
		for tweet in stream:
			#Tweet should be lowercased or not?
			f.write(" ".join(tweet).encode("utf-8").lower()+"\n")

	print "Running brown clustering."
	cluster_command = "./brown-cluster/wcluster"
	args = [cluster_command,
			"--text", in_fn,
			"--c", str(c),
			"--output_dir", out_dir
		]

	code = subprocess.call(args)

	print "Removing temp input file."
	try:
		os.remove(in_fn)
	except Exception, e:
		print "Couldnt remove file:",str(e)
	print "Done."


def usage():
	print "Usage:"
	print "build_brown_clusters.py -i <input_file> -c <num_clusters> -o <output_directory>"
	sys.exit()

def handle_args(argv):
	input_file = None
	c = None
	output_directory = "./output"
	try:
		opts, args = getopt.getopt(argv,"hi:c:o:",["input_file=","num_clusters=","output_directory="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			usage()
		elif opt in ("-i", "--input_file"):
			input_file = arg
			#TODO: validate file exists
		elif opt in ("-o", "--output_directory"):
			output_directory = arg
		elif opt in ("-c", "--num_clusters"):
			c = int(arg)

	if input_file and c:
		return input_file, c, output_directory
	else:
		usage()

if __name__ == "__main__":
	input_file, c, out_dir = handle_args(sys.argv[1:])
	run_brown_clustering(input_file, c, out_dir)
