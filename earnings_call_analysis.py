from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


# Method that implements NLP pipeline of cleaning text
def clean_earnings_call_transcript(local_file):
    transcript_read = open(local_file, 'r')
    transcript_text = transcript_read.read()

    print(transcript_text)


clean_earnings_call_transcript('crm_earnings_transcript_clean.txt')