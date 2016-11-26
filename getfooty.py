#! /usr/bin/env python3

import json, re, requests, sys, datetime
#from prettytable import PrettyTable


class objAPI():
    def __init__(self):
        self.apikey = '76f8d5e93e754aa0b89701f0c95c368c'
        self.tokenheaders = {'X-Auth-Token': self.apikey, 'X-Response-Control': 'minified'}

    def get(self,api):
        try:
            url = 'http://api.football-data.org/v1/'+api
            resp = requests.get(url, self.apikey, headers=self.tokenheaders)
            resp.raise_for_status()
            return resp
        except:
            print("Something wrong to GET /", api)
            sys.exit()




#testobj = objAPI()
#testresult = testobj.get('competitions/')

#print(testresult.text)


#APIKey = '76f8d5e93e754aa0b89701f0c95c368c'

#url = 'http://api.football-data.org/v1/'
#headers = { 'X-Auth-Token': APIKey, 'X-Response-Control': 'minified' }
