import requests

def scrape(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(url, headers=headers)
    return str(result.text)

def chunkParser(scrape, needle):
    ind = scrape.find(needle)
    return scrape[ind:ind+60]