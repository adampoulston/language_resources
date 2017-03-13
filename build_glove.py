# -*- coding: UTF-8 -*-
import os, sys, getopt, subprocess, gzip, json
from GZIPTweetStream import GZIPTweetStream

def run_glove(input_file, out_dir):

    #Create temporary directories to store input/output files
    in_dir = "./glove_input"

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
    in_fn = "inputfile.txt"
    in_fn = in_dir+"/"+in_fn
    tboundary = " "+" ".join(["tboundary"]*5)+" "
    with open(in_fn,"w+") as f:
        for tweet in stream:
            #Write to file with five dummy words between sentences (as per docs)
            f.write(" ".join(tweet).encode("utf-8")+tboundary)


    #glove args definition
    corpus = in_fn
    glove_dir = "./GloVe"
    vocab_file=out_dir+"/vocab.txt"
    cooccurrence_file=out_dir+"/cooccurrence.bin"
    cooccurrence_shuf_file=out_dir+"/cooccurrence.shuf.bin"
    builddir=glove_dir+"/build"
    save_file=out_dir+"/vectors"
    verbose=2
    memory=4.0
    vocab_min_count=5
    vector_size=50
    max_iter=15
    window_size=15
    binary=2
    num_threads=6
    x_max=10

    #ensure list only contains strings
    l2sl = lambda x:[str(el) for el in x]

    vocab_args = l2sl([builddir+"/vocab_count", "-min-count", vocab_min_count, "-verbose", verbose])
    coocur_args = l2sl([builddir+"/cooccur", "-memory", memory, "-vocab-file", vocab_file, "-verbose", verbose, "-window-size", window_size])
    shuffle_args = l2sl([builddir+"/shuffle", "-memory", memory, "-verbose", verbose])
    glove_args = l2sl([builddir+"/glove", "-save-file", save_file, "-threads", num_threads, "-input-file", cooccurrence_shuf_file, "-x-max", x_max, "-iter", max_iter, "-vector-size", vector_size, "-binary", binary, "-vocab-file", vocab_file, "-verbose", verbose])

    print "Calling:"," ".join(vocab_args)
    vocab_res = subprocess.call(vocab_args,stdin=open(corpus,"rb"),stdout=open(vocab_file, "w+"))
    print "Calling coocurrence process"
    coocur_res = subprocess.call(coocur_args,stdin=open(corpus,"rb"),stdout=open(cooccurrence_file, "w+"))
    print "Calling shuffle process."
    shuffle_res = subprocess.call(shuffle_args,stdin=open(cooccurrence_file,"rb"),stdout=open(cooccurrence_shuf_file,"w+"))
    print "Calling glove process."
    glove_res = subprocess.call(glove_args)
    print "Fin."
# DEPRECATED
# def usage():
#     print "Usage:"
#     print "build_glove.py -i <input_file> -o <output_directory>"
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
#         elif opt in ("-o", "--output_directory"):
#             output_directory = arg
#
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

    run_glove(args.input, args.out_dir)
