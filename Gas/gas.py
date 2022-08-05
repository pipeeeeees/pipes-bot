import webscraper as ws

state_dict = {
    'Alabama' : 'AL',
    'Alaska' : 'AK',
    'Arizona' : 'AZ',
    'Arkansas' : 'AR',
    'California' : 'CA',
    'Colorado' : 'CO',
    'Connecticut' : 'CT',
    'Delaware' : 'DE',
    'Florida' : 'FL',
    'Georgia' : 'GA',
    'Hawaii' : 'HI',
    'Idaho' : 'ID',
    'Illinois' : 'IL',
    'Indiana' : 'IN',
    'Iowa' : 'IA',
    'Kansas' : 'KS',
    'Kentucky' : 'KY',
    'Louisiana' : 'LA',
    'Maine' : 'ME',
    'Maryland' : 'MD',
    'Massachusetts' : 'MA',
    'Michigan' : 'MI',
    'Minnesota' : 'MN',
    'Mississippi' : 'MS',
    'Missouri' : 'MO',
    'Montana' : 'MT',
    'Nebraska' : 'NE',
    'Nevada' : 'NV',
    'New Hampshire' : 'NH',
    'New Jersey' : 'NJ',
    'New Mexico' : 'NM',
    'New York' : 'NY',
    'North Carolina' : 'NC',
    'North Dakota' : 'ND',
    'Ohio' : 'OH',
    'Oklahoma' : 'OK',
    'Oregon' : 'OR',
    'Pennsylvania' : 'PA',
    'Rhode Island' : 'RI',
    'South Carolina' : 'SC',
    'South Dakota' : 'SD',
    'Tennessee' : 'TN',
    'Texas' : 'TX',
    'Utah' : 'UT',
    'Vermont' : 'VT',
    'Virginia' : 'VA',
    'Washington' : 'WA',
    'West Virginia' : 'WV',
    'Wisconsin' : 'WI',
    'Wyoming' : 'WY'
}

def get_gas(fullname_or_abbr):
        if len(fullname_or_abbr) == 2:
            mylist = ws.BigChunkParser(ws.scrape('https://gasprices.aaa.com/?state='+fullname_or_abbr),
                                            'Current Avg.').replace('</td>','').split('<td>')
            return mylist[1][0:6],mylist[2][0:6],mylist[3][0:6],mylist[4][0:6]
        else:
            abbr = state_dict[fullname_or_abbr]
            mylist = ws.BigChunkParser(ws.scrape('https://gasprices.aaa.com/?state='+abbr),
                                            'Current Avg.').replace('</td>','').split('<td>')
            return mylist[1][0:6],mylist[2][0:6],mylist[3][0:6],mylist[4][0:6]

def get_gas_msg(fullname_or_abbr):
        if len(fullname_or_abbr) == 2:
            mylist = ws.BigChunkParser(ws.scrape('https://gasprices.aaa.com/?state='+fullname_or_abbr),
                                            'Current Avg.').replace('</td>','').split('<td>')
            reg,mid,prem,die = mylist[1][0:6],mylist[2][0:6],mylist[3][0:6],mylist[4][0:6]
            msg = f'Today in the state of {get_key(fullname_or_abbr, state_dict)}, the state-wide average gas prices are:\n\t\tRegular: {reg}\n\t\tMidgrade: {mid}\n\t\tPremium: {prem}\n\t\tDiesel: {die}\nSource: https://gasprices.aaa.com/?state={fullname_or_abbr}'
            return msg
        elif len(fullname_or_abbr) >= 4:
            abbr = state_dict[fullname_or_abbr]
            mylist = ws.BigChunkParser(ws.scrape('https://gasprices.aaa.com/?state='+abbr),
                                            'Current Avg.').replace('</td>','').split('<td>')
            reg,mid,prem,die = mylist[1][0:6],mylist[2][0:6],mylist[3][0:6],mylist[4][0:6]
            msg = f'Today in the state of {fullname_or_abbr}, the state-wide average gas prices are:\n\t\tRegular: {reg}\n\t\tMidgrade: {mid}\n\t\tPremium: {prem}\n\t\tDiesel: {die}\nSource: https://gasprices.aaa.com/?state={abbr}'
            return msg
        else:
            return f'Error. Entered in: {fullname_or_abbr}'

def get_key(val, my_dict):
    for key, value in my_dict.items():
         if val == value:
             return key