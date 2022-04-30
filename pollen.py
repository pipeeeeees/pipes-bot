import webscraper as ws

def getPollenCount():
    mylist = ws.chunkParser(ws.scrape('https://www.atlantaallergy.com/pollen_counts'),
                                      'class="pollen-num"').split(' ')
    if len(mylist) > 0:
        for i in mylist:
            try:
                j = int(i)
                return j
            except:
                continue
    if mylist == ['']:
        return 'The pollen count in Atlanta has not been reported yet. Please try again later.'
    print(mylist)
    return 69420