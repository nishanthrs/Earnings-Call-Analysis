from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import spacy
import string
from collections import Counter

# nltk.download('stopwords')
nlp = spacy.load('en')


def tokenize_and_clean_transcript(local_file):
    '''
    Method that implements NLP pipeline of cleaning text:
    1. Tokenization
    2. Removing stopwords
    3. Lemmatization

    Args: name of earnings call transcript file, new stop words

    Returns: list of tokens (spacy doc) and list of lemmatized words (list of strings)
    '''

    punctuation = string.punctuation
    stopwords = spacy.lang.en.stop_words.STOP_WORDS

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
    print(transcript_text)
    return (transcript_doc, transcript_text)


def analyze_transcript(transcript_doc, transcript_text, k):
    '''
    Method that get k most frequent words of earnings call transcript

    Args: spacy doc of transcript and text of transcript

    Returns: list of k most frequent words
    '''

    # five most common tokens
    word_freq = Counter(transcript_text)
    common_words = word_freq.most_common(k)

    # five most common noun tokens
    nouns = [token.lemma_ for token in transcript_doc if token.pos_ == 'NOUN']
    noun_freq = Counter(nouns)
    common_nouns = noun_freq.most_common(k)

    print("Common words: ", common_words)
    print("Common nouns: ", common_nouns)


crm_transcript_doc, crm_transcript_text = tokenize_and_clean_transcript(
    'crm_earnings_transcript_clean_2.txt')
analyze_transcript(crm_transcript_doc, crm_transcript_text, 10)