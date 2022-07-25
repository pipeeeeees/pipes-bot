import requests

def yeezyQuote():
    return str(requests.get('https://api.kanye.rest').text)[10:].split('"')[0]
