# -*- coding: UTF-8 -*-
import os, sys, getopt, subprocess, gzip, json, argparse
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
