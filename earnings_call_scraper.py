import requests
import html2text
'''
# References: 
#   1. Scraping Seeking Alpha pages: https://stackoverflow.com/questions/48756326/web-scraping-results-in-403-forbidden-error
#   2. Free proxies: https://free-proxy-list.net
'''

r = requests.get(
    'https://seekingalpha.com/article/4236893-microsoft-corp-msft-ceo-satya-nadella-q2-2019-results-earnings-call-transcript?part=single',
    proxies={
        'http': '50.207.31.221:80'
    }).text

msft = open('msft_earnings_transcript.txt', 'w+')
msft.write(r)
msft.close()

msft_read = open('msft_earnings_transcript.txt', 'r')
# print(msft_read.read())

cleaned_earnings_transcript = html2text.html2text(msft_read.read())
msft_read.close()
# print(cleaned_earnings_transcript)
msft_clean = open('msft_earnings_transcript_clean.txt', 'w+')
msft_clean.write(cleaned_earnings_transcript)
msft_clean.close()
