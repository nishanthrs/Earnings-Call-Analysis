import requests
import html2text
import random
'''
# References: 
#   1. Scraping Seeking Alpha pages: https://stackoverflow.com/questions/48756326/web-scraping-results-in-403-forbidden-error
#   2. Free proxies: https://free-proxy-list.net
'''


def get_rand_ip_address():
    free_proxies = [
        '138.0.229.213', '103.245.204.58', '139.59.56.112', '128.199.204.244',
        '54.39.235.238', '103.109.75.189'
    ]
    return random.choice(free_proxies)


def get_earnings_call_transcript(transcript_uri):
    successful_req = False
    while not successful_req:
        try:
            rand_proxy = get_rand_ip_address()
            print("Proxy used: ", rand_proxy)
            r = requests.get(transcript_uri, proxies={'http': rand_proxy}).text
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

    crm = open('crm_earnings_transcript.txt', 'w+')
    crm.write(r)
    crm.close()


def clean_earnings_call_transcript_html(local_file):
    crm_read = open(local_file, 'r')
    # print(crm_read.read())

    cleaned_earnings_transcript = html2text.html2text(crm_read.read())
    crm_read.close()
    # print(cleaned_earnings_transcript)
    crm_clean = open('crm_earnings_transcript_clean.txt', 'w+')
    crm_clean.write(cleaned_earnings_transcript)
    crm_clean.close()


get_earnings_call_transcript(
    'https://seekingalpha.com/article/4246320-salesforce-com-inc-crm-ceo-marc-benioff-q4-2019-results-earnings-call-transcript'
)

clean_earnings_call_transcript_html('crm_earnings_transcript.txt')