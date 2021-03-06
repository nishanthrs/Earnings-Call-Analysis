#!/usr/bin/env python3

import spacy
import string
from collections import Counter
import os

nlp = spacy.load('en')
# TODO: Continue to remove more stopwords (i.e. company name, 'quarter', 'year', '%', etc.)
# People say 'thank you' way too much in earnings calls!
new_stopwords = ['thank', 'quarter', 'year', '’s', '%']


def add_stopwords(stopwords, new_stopwords):
    """
    Method that adds new stopwords to list of spacy default stopwords

    Args:
    stopwords - spacy default stopwords
    new_stopwords - new stopwords

    Returns: new list of stopwords
    """

    for new_stopword in new_stopwords:
        stopwords.add(new_stopword)
    return stopwords


def tokenize_and_clean_transcript(local_file, new_stopwords):
    """
    Method that implements NLP pipeline of cleaning text:
    1. Tokenization
    2. Removing stopwords
    3. Lemmatization

    Args: 
    local_file - name of earnings call transcript file
    new_stopwords - new stop words to filter doc with

    Returns: list of tokens (spacy doc) and list of lemmatized words (list of strings)
    """

    punctuation = string.punctuation
    stopwords = spacy.lang.en.stop_words.STOP_WORDS
    stopwords = add_stopwords(stopwords, new_stopwords)

    transcript_read = open(local_file, 'r')
    transcript_doc = nlp(transcript_read.read())
    transcript_text = [token.lemma_ for token in transcript_doc]
    transcript_text = [
        tok.lemma_.lower().strip()
        for tok in transcript_doc
        if tok.lemma_ != '-PRON-'
    ]
    transcript_text = [
        tok for tok in transcript_text
        if tok not in stopwords and tok not in punctuation
    ]

    return (transcript_doc, transcript_text)


def get_freq_terms(transcript_doc, transcript_text, k):
    """
    Method that get k most frequent words of earnings call transcript

    Args: 
    transcript_doc - spacy doc of transcript
    transcript_text - text of transcript
    k - k most common frequent terms

    Returns: list of k most frequent words
    """

    # five most common tokens
    word_freq = Counter(transcript_text)
    common_words = word_freq.most_common(k)

    # five most common noun tokens
    nouns = [token.lemma_ for token in transcript_doc if token.pos_ == 'NOUN']
    noun_freq = Counter(nouns)
    common_nouns = noun_freq.most_common(k)

    # five most common verb tokens
    verbs = [token.lemma_ for token in transcript_doc if token.pos_ == 'VERB']
    verb_freq = Counter(verbs)
    common_verbs = verb_freq.most_common(k)

    return (common_words, common_nouns, common_verbs)


def write_freq_words_to_file(analysis_dir, local_file, common_terms):
    """
    Method that writes the most frequent terms from the document to a file

    Args:
    analysis_dir - directory of frequent terms of earnings transcripts
    local_file - name of file to write frequent terms to
    common_terms - list of frequent terms

    Returns: None
    """

    if not os.path.exists(analysis_dir):
        os.makedirs(analysis_dir)
    freq_words_file_path = analysis_dir + '/' + local_file
    freq_words_file = open(freq_words_file_path, 'w+')

    for terms in common_terms:
        for term in terms:
            freq_words_file.write(str(term) + ' ')
        freq_words_file.write('\n')

    freq_words_file.close()


def exec_doc_analysis(docs_dir, analysis_dir):
    """
    Method that executes the entire transcript analysis to get most frequent words

    Args: 
    docs_dir - directory of transcripts
    analysis_dir - directory of transcript analysis files
    transcript_filename - transcript filename

    Returns: None
    """

    docs_filenames = [f for f in os.listdir(docs_dir) if os.path.isfile(os.path.join(docs_dir, f))]
    for doc_filename in docs_filenames:
        doc_path = os.path.join(docs_dir, doc_filename)
        doc, doc_text = tokenize_and_clean_transcript(
            doc_path, new_stopwords)
        common_terms = get_freq_terms(doc, doc_text, 10)
        write_freq_words_to_file(
            analysis_dir,
            '{}_freq_words.txt'.format(os.path.splitext(doc_filename)[0]),
            common_terms
        )


docs_dir = '../earnings_call_transcripts/tndm/'
analysis_dir = '../nlp_analyis'
exec_doc_analysis(docs_dir, analysis_dir)
