import requests

def yeezy_quote():
    return str(requests.get('https://api.kanye.rest').text)[10:].split('"')[0]
