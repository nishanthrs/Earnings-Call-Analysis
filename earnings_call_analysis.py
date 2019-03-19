from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import spacy

# nltk.download('stopwords')
# stopwords = spacy.lang.en.stop_words.STOP_WORDS
nlp = spacy.load('en')
punct_marks = ['.', ',', '?', '!', '*', '-', '\n', '\n\n']


def add_punct_stopwords(punct_marks):
    for punct in punct_marks:
        nlp.vocab[punct].is_stop = True


# Method that implements NLP pipeline of cleaning text
def clean_earnings_call_transcript(local_file):
    transcript_read = open(local_file, 'r')

    # 1. Tokenize
    transcript_text = nlp(transcript_read.read())
    # 2. Remove stopwords
    add_punct_stopwords(punct_marks)
    transcript_text = [
        token.text for token in transcript_text if not token.is_stop
    ]
    print(transcript_text)
    # 3. Lemmatization


clean_earnings_call_transcript('crm_earnings_transcript_clean_2.txt')