# -*- coding: UTF-8 -*-
import os, sys, getopt, subprocess, gzip, json
from GZIPTweetStream import GZIPTweetStream
from gensim.models import Word2Vec

def run_w2v(input_file, out_dir):
	try:
		os.makedirs(out_dir)
	except Exception, e:
		print "Didnt create output dir (",str(e),")"

	#stream text from gzipped json file
	stream = GZIPTweetStream([input_file])

	#build W2V model
	w2v = Word2Vec(stream)
	w2v.save(out_dir+"/"+"model.w2v")


def usage():
	print "Usage:"
	print "build_w2v.py -i <input_file> -o <output_directory>"
	sys.exit()

def handle_args(argv):
	input_file = None
	c = None
	output_directory = "./output"
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["input_file=","output_directory="])
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

	if input_file:
		return input_file, output_directory
	else:
		usage()

if __name__ == "__main__":
	input_file, out_dir = handle_args(sys.argv[1:])
	run_w2v(input_file, out_dir)
