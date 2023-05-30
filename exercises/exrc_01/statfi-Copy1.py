
##### imports #####

import requests
import json
import sys 

from googletrans import Translator
from functools import partial

from copy import deepcopy


##### config #####

finnish = True
# finnish = False


##### helpers #####

query_template = {
    "query": [], # list of query items
    "response": {
        "format": "json"
    }
}

query_item_template = {
    "code": "", # variable
    "selection": {
        "filter": "item",
        "values": [] # list of strings
    }
}


##### main #####

translator = Translator()
tr = partial(translator.translate, src='fi', dest='en')

with requests.Session() as session:

    # first, some browsing in order to get the correct database
    # you can do this with a browser too (but translation may become an issue)
    response = session.get('https://pxdata.stat.fi/PXWeb/api/v1/fi/StatFin/')
    for item in response.json():
        item_text = item['text'] if finnish else tr(item['text']).text
        print(item['id'], item_text)

    sys.exit()
    # execution stops here now

    # next, append the id of your thing of interest to the url
     response = session.get('https://pxdata.stat.fi/PXWeb/api/v1/fi/StatFin/adopt')
         response = session.get('https://pxdata.stat.fi/PXWeb/api/v1/fi/StatFin/vamuu')
             for item in response.json():
    print(item)
    sys.exit()

    # once you know what .px file you want, comment all the above out and continue

    # fetch the final px filename with another get request
    response = session.get('https://pxdata.stat.fi/PXWeb/api/v1/fi/StatFin/adopt/statfin_adopt_pxt_11lv.px')
    # response = session.get('https://pxdata.stat.fi/PXWeb/api/v1/fi/StatFin/vamuu/statfin_vamuu_pxt_11lj.px')

    # this should give you the available variable names (~ headers)
    # those could still be obtained by browser browsing as well
    # session.get is like entering the url in a browser
    myjson = response.json()
    print(myjson.keys())
    print(len(myjson['variables']))
    for var in myjson['variables']:
        print(var['text'])


    # okay, but then build the actual query for the data

    # first, fetch the maximum values that one can download
    # kind of hi-tech, got it from the documentation
    # (the documentation typically sucks in free & public apis like this)
    response = session.get('https://statfin.stat.fi/PXWeb/api/v1/fi/?config')
    maxvalues = response.json()['maxValues']

    # query building
    # please edit only the "for myvar" line
    query = query_template.copy()
    total_values = 1
    for myvar in ['Vuosi','Sukupuoli','Ikä','Syntymävaltio']: # edit
        for myvar in ['Kuukausi','Ikä','Tiedot']: # edit
        myvalues = []
        query_item = deepcopy(query_item_template)
        for v in myjson['variables']:
            if v['code'] == myvar:
                myvalues = v['values']
        total_values = total_values * len(myvalues)
        query_item['code'] = myvar
        query_item['selection']['values'] = myvalues
        query['query'].append(query_item)
    if total_values > maxvalues:
        print('your query is too big, try again with fewer variables')
        sys.exit()


    # obtain the actual data with a "post" request
    # that's like submitting a web form
    # and cannot be done by browsing anymore
    response = session.post('https://pxdata.stat.fi/PXWeb/api/v1/fi/StatFin/adopt/statfin_adopt_pxt_11lv.px', json=query)
    # response = session.post('https://pxdata.stat.fi/PXWeb/api/v1/fi/StatFin/vamuu/statfin_vamuu_pxt_11lj.px')

    # dump the data into a file
    myjson = response.json()
    with open('test.json', 'w') as handle:
        json.dump(myjson, handle, indent=4)

