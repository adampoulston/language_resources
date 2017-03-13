# -*- coding: UTF-8 -*-
import os, sys, getopt, subprocess, gzip, json, argparse
from GZIPTweetStream import GZIPTweetStream

def run_brown_clustering(input_file, c, out_dir):
    c = 5

    #Create temporary directories to store input/output files
    in_dir = "./input"

    try:
        os.makedirs(in_dir)
    except Exception, e:
        print "Didnt create temp input dir (",str(e),")"

    try:
        os.makedirs(out_dir)
    except Exception, e:
        print "Didnt create temp output dir (",str(e),")"


    #extract text from gzipped json file
    #write texts to temp file, tokens separated by spaces, one text per line
    stream = GZIPTweetStream([input_file])
    in_fn = "inputfile"
    with open(in_dir+"/"+in_fn,"w+") as f:
        for tweet in stream:
            f.write(" ".join(tweet).encode("utf-8")+"\n")

    cluster_command = "./brown-cluster/wcluster"
    args = [cluster_command,
            "--text", in_dir+"/"+in_fn,
            "--c", str(c),
            "--output_dir", out_dir
        ]

    code = subprocess.call(args)

# Deprecated
# def usage():
# 	print "Usage:"
# 	print "build_brown_clusters.py -i <input_file> -c <num_clusters> -o <output_directory>"
# 	sys.exit()
#
# def handle_args(argv):
# 	input_file = None
# 	c = None
# 	output_directory = "./output"
# 	try:
# 		opts, args = getopt.getopt(argv,"hi:c:o:",["input_file=","num_clusters=","output_directory="])
# 	except getopt.GetoptError:
# 		usage()
# 		sys.exit(2)
# 	for opt, arg in opts:
# 		if opt == '-h':
# 			usage()
# 		elif opt in ("-i", "--input_file"):
# 			input_file = arg
# 			#TODO: validate file exists
# 		elif opt in ("-o", "--output_directory"):
# 			output_directory = arg
# 		elif opt in ("-c", "--num_clusters"):
# 			c = int(arg)
#
# 	if input_file and c:
# 		return input_file, c, output_directory
# 	else:
# 		usage()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    description = """
    Usage:
    "build_brown_clusters.py -i <input_file> -c <num_clusters> -o <output_directory>"
    """)

    parser.add_argument('-i', '--input', help = "Input file")
    parser.add_argument('-c', '--clusters', help = "Number of clusters")
    parser.add_argument('-o', '--out_dir', help = "Output directory")
    args = parser.parse_args()

    while not os.path.exists(args.input):
        args.input = input("The file does not exist. Please provide me with the actual file")

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    run_brown_clustering(args.input, args.clusters, args.out_dir)
