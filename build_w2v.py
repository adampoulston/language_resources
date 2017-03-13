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

# DEPRECATED
# def usage():
#     print "Usage:"
#     print "build_w2v.py -i <input_file> -o <output_directory>"
#     sys.exit()
#
# def handle_args(argv):
#     input_file = None
#     c = None
#     output_directory = "./output"
#     try:
#         opts, args = getopt.getopt(argv,"hi:o:",["input_file=","output_directory="])
#     except getopt.GetoptError:
#         usage()
#         sys.exit(2)
#     for opt, arg in opts:
#         if opt == '-h':
#             usage()
#         elif opt in ("-i", "--input_file"):
#             input_file = arg
#             #TODO: validate file exists
#
#         elif opt in ("-o", "--output_directory"):
#             output_directory = arg
#
#     if input_file:
#         return input_file, output_directory
#     else:
#         usage()

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

    run_w2v(args.input, args.out_dir)
