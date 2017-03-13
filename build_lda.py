import os, sys, json, argparse
from gensim import models
from GZIPTweetStream import GZIPTweetStream

def _create_corpus(source, out_dir, fp):
    """
    Create corpus here if it doesn't exist, otherwise load it into memory
    :fp: Filename of corpus file
    :corp_fp: Filename of the corpus file to load/save
    """

    if os.path.exists(cfg.BASE + cfg.MATRIX_PATH + corp_fp + '.corp.mm'):
        print("Corpus exists, load into memory...", file=sys.stdout)
        return corpora.MmCorpus(out_dir + '/' + fp + '.corp.mm')
    else:
        dictionary = _create_dictionary(fp, corp_fp)
        corpus = [dictionary.doc2bow(text) for text in GZIPTweetStream([source])]
        corpora.MmCorpus.serialize(out_dir + '/' + fp + '.corp.mm', corpus)
        return corpus

def create_dictionary(source, out_dir, fp):
    """
    Create and save dictionary for LDA if it does not already exist
    :source: Data set to read in
    :out_dir: Directory to write output to
    """
    if os.path.exists(out_dir + fp):
        print("Dicionary exists, load into memory...", file=sys.stdout)
        return corpora.Dictionary.load(out_dir + '/' + fp)
    else:
        # TODO Test which one works the first one should require less memory
        dictionary = corpora.Dictionary(GZIPTweetStream([source]))
        # dictionary = corpora.Dictionary([item for item in GZIPTweetStream([source])])

        dictionary.save(out_dir + '/' + dict_fp)

    return dictionary


def train_lda(source, passes, topics, workers, out_dir):
    print("Create corpus...", file = sys.stdout)
    dictionary = create_dictionary(source, out_dir)
    corpus = create_corpus(source, out_dir)

    print("Training model...", file = sys.stdout)
    lda = models.ldamulticore.LdaMulticore(
            corpus,
            num_topics = topics,
            id2word = dictionary,
            workers = workers,
            passes = passes
            )

    print("Save model...", file = sys.stdout)
    lda.save(out_dir + '/lda-{0}topics-{1}passes-{2}workers.model'.format(topics, passes, workers))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    description = """ Run LDA on multiple cores

        Options:
        --workers: Number of cores to use
        --topics: Number of topics to extract
        --passes: Number of passes over the data set
        --source: The file to be processed
        --outdir: The output directory to contain the model, corpus, and dictionary
    """)

    parser.add_argument('--workers', type=int, nargs = 1)
    parser.add_argument('--topics' , type=int, nargs = 1)
    parser.add_argument('--passes' , type=int, nargs = 1)
    parser.add_argument('--source' , type=str)
    args = parser.parse_args()

    train_lda(source = args.source, passes = args.passes, topics = args.topics, workers = args.workers)
