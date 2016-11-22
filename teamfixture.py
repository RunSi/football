#! /usr/bin/env python3
__author__ = 'sihart'

__author__ = 'sihart'

import json, re, requests, sys
from prettytable import PrettyTable
#Pretty table information - https://code.google.com/archive/p/prettytable/wikis/Tutorial.wiki

APIKey = '76f8d5e93e754aa0b89701f0c95c368c'  #API Key obtained from api.football-data.org


url = 'http://api.football-data.org/v1/soccerseasons/426/leagueTable'
headers = { 'X-Auth-Token': APIKey, 'X-Response-Control': 'minified' }

datepattern = re.compile(r'^(.*?)((19|20)\d\d)-((0|1)\d)-((0|1|2|3)?\d)T((\d\d:\d\d):\d\dZ)(.*?)$')
datedict = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}


def mangledate(date):               #The date is in a rubbish format, so this function will make it more readable
    mo = datepattern.search(date)
    year = mo.group(2)
    month = mo.group(4)
    day = mo.group(6)
    time = mo.group(9)
    newdate = day + ' ' + datedict[int(month)] + '  ' + year
    return newdate, time


if len(sys.argv) < 2:       #check to see if there are any arguments after the command, if not print message
    print( '\nUsage teamfixture.py teamname or List\n')
    sys.exit()

#TODO: Use team ID instead of listing, also pprint
if (sys.argv[1]) == ('list'):       #if argument is list, print out correct team name references
    print( '\nLiverpool\n','Chelsea\n''ManCity\n','Arsenal\n','Spurs\n','ManU\n','Everton\n','Watford\n','Burnley\n','Southampton\n','West Bromwich\n','Stoke\n','Bournemouth\n','Foxes\n','Middlesbrough\n','Crystal\n','West Ham\n','Hull\n','Swans\n')
    sys.exit()

club = ' '.join(sys.argv[1:])   #club variable used to identify teamId.  Join used where team name is more than two arguments, e.g. West Ham

response = requests.get(url, headers=headers) #Retrieve JSON data for the EPL table, this will provide teamId data.
response.raise_for_status()

footdata = json.loads(response.text)  #parse JSON into strings and dicts.
teamdata = footdata['standing'] #teamdata will contain the dictionary value for Standing. This value is all 20 EPL teams
count1 = len(teamdata) #should count to 20

for i in range(count1):             #iterate over Standing value to look for a match between variable club with
    teamname = (teamdata[i]['team'])
    if teamname == club:
        Id = (teamdata[i]['teamId'])    #if club and teamname match then invoke variable Id to equal teamId



# Next part
try:
    url2 = 'http://api.football-data.org/v1/teams/%s/fixtures' % Id #The url here will return fixturesJSON data for the teamId
                                                                    #using the Id variable in the url string


except NameError:                                   #If the club variable was not matched against team and thus no Id,
    print('\nNonsense Team Name\n')                 #Then catch NameError traceback and print response. Exit program.
    sys.exit()

response = requests.get(url2, headers=headers)      #retrieve fixtures data from url2
response.raise_for_status()
whudata = json.loads(response.text)                 #parse JSON into strings and dicts.

fixtures = whudata['fixtures']                      #fixtures variable will hold data from fixtures key



count = len(fixtures)                               #count the number of fixtures in fixtures variable
x = PrettyTable(["Home Team", "V", "AwayTeam", "Date","Time"])  #create a table to populate
x.align["Home Team"]="l"
x.align["AwayTeam"]="l"

print('Upcoming Fixtures - \n')
for i in range(count):              #iterate over fixtures
    finish = (fixtures[i]['status'])
    if finish == 'FINISHED':        #if the status key is FINISHED then ignore
        continue
    else:                           #populate the table with fixtures which do not have a status of FINISHED
        date1 = (fixtures[i]['date'])
        hometeam = fixtures[i]['homeTeamName']
        awayteam = fixtures[i]['awayTeamName']
        x.add_row([hometeam, "v", awayteam, mangledate(date1)[0],mangledate(date1)[1]])
        x.add_row(["","","","",""])


print(x)    #print the PrettyTable



