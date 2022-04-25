import webscraper as ws

def getGaGas():
    mylist = ws.BigChunkParser(ws.scrape('https://gasprices.aaa.com/?state=GA'),
                                      'Current Avg.').replace('</td>','').split('<td>')
    
    try:
        return mylist[1][0:6],mylist[2][0:6],mylist[3][0:6],mylist[4][0:6]
    except:
        return 'HTML ERROR','HTML ERROR','HTML ERROR','HTML ERROR'

def getGaGasTX():
    mylist = ws.BigChunkParser(ws.scrape('https://gasprices.aaa.com/?state=TX'),
                                      'Current Avg.').replace('</td>','').split('<td>')
    
    try:
        return mylist[1][0:6],mylist[2][0:6],mylist[3][0:6],mylist[4][0:6]
    except:
        return 'HTML ERROR','HTML ERROR','HTML ERROR','HTML ERROR'