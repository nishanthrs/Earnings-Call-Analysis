import requests
import html2text
import random
import re
import os
'''
# References: 
#   1. Scraping Seeking Alpha pages: https://stackoverflow.com/questions/48756326/web-scraping-results-in-403-forbidden-error
#   2. Free proxies: https://free-proxy-list.net]

# Look into additional storage options: local filesystems, cloud filesystems, SQL or NoSQL databases
# For now, since the files aren't too large, we'll use a 
# Requirements of storage option: store large number of small files, quick access/lookup time (read operation)
'''


def get_rand_ip_address():
    free_proxies = [
        '138.0.229.213', '103.245.204.58', '139.59.56.112', '128.199.204.244',
        '54.39.235.238', '103.109.75.189'
    ]
    return random.choice(free_proxies)


def create_filename(transcript_uri):
    transcript_metadata = transcript_uri.split('-')
    stock_symbol_idx = transcript_metadata.index('ceo') - 1
    stock_symbol = transcript_metadata[stock_symbol_idx]
    date = [q for q in transcript_metadata if re.match(r'\b(q[1-4])\b', q)][0]
    year = [q for q in transcript_metadata if re.match(r'\b(\d{4})\b', q)][0]

    transcript_filename = stock_symbol + '_earnings_transcript_' + date + '_' + year + '.txt'

    return transcript_filename


def get_earnings_call_transcript(transcript_uri, transcript_filename):
    successful_req = False
    while not successful_req:
        try:
            rand_proxy = get_rand_ip_address()
            print("Proxy used: ", rand_proxy)
            r = requests.get(transcript_uri, proxies={'http': rand_proxy}).text
            # TODO: add mechanism here to keep successful_req as False if robot page appears
            successful_req = True
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Technical Details given below.\n")
            print(str(e))
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
        except KeyboardInterrupt:
            print("Someone closed the program")
            break

    transcript = open(transcript_filename, 'w+')
    transcript.write(r)
    transcript.close()


def clean_earnings_call_transcript_html(local_file, clean_file):
    transcript_read = open(local_file, 'r')
    cleaned_earnings_transcript = html2text.html2text(transcript_read.read())
    transcript_read.close()
    os.remove(local_file)

    print(cleaned_earnings_transcript)

    stock_symbol = clean_file.split('_')[0]
    stock_dir = '../earnings_call_transcripts/' + stock_symbol
    if not os.path.exists(stock_dir):
        stock_dir = '../earnings_call_transcripts/' + stock_symbol
        os.makedirs(stock_dir)
    transcript_path = stock_dir + '/' + clean_file
    transcript_clean = open(transcript_path, 'w+')

    a_1 = re.search(r'\b(Company Participants)\b', cleaned_earnings_transcript)
    a_2 = re.search(r'\b(Executives)\b', cleaned_earnings_transcript)
    if a_1 == None:
        a = a_2.start()
    else:
        a = a_1.start()
    b = re.search(r'\b(Follow SA Transcripts and get email alerts)\b',
                  cleaned_earnings_transcript).start()

    transcript_clean.write(cleaned_earnings_transcript[(a - 2):b])
    transcript_clean.close()


def scrape_clean_transcript(transcript_uri):
    get_earnings_call_transcript(
        transcript_uri, '../earnings_call_transcripts/transcript_html.txt')

    transcript_filename = create_filename(transcript_uri)
    clean_earnings_call_transcript_html(
        '../earnings_call_transcripts/transcript_html.txt', transcript_filename)


'''
scrape_clean_transcript(
    'https://seekingalpha.com/article/4244554-tandem-diabetes-care-inc-tndm-ceo-kim-blickenstaff-q4-2018-results-earnings-call-transcript?part=single'
)
'''
scrape_clean_transcript(
    'https://seekingalpha.com/article/4217453-tandem-diabetes-care-inc-tndm-ceo-kim-blickenstaff-q3-2018-results-earnings-call-transcript'
)
