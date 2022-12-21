import Gas.webscraper as ws

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
        return "The pollen count in Atlanta has not been reported yet. Please try again later.\n\nNote: Atlanta's pollen count is not reported on the weekends (outside of pollen season).\nhttps://www.atlantaallergy.com/pollen_counts"
    print(mylist)
    return 69420