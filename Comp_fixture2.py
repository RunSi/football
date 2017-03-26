#! /usr/bin/env python3

### Authoured by Simon Hart - 26th November 2016 ###
### API provided by api.football-data.org ###

import getfooty, json, sys, datetime, re, subprocess
from prettytable import PrettyTable


### by defining main then all variables in the code will remain local in scope to this code, unless explicitly returned
###
def main():


### this 'rough' regular expression will locate date values in any returned JSON
    datepattern = re.compile(r'^(.*?)(((19|20)\d\d)-((0|1)\d)-((0|1|2|3)?\d))T((\d\d:\d\d):\d\dZ)(.*?)$')

### the returned date values are shit.  This will convert into user friendly format
    def convertdate(date):
        mo = datepattern.search(date)
        date1 = mo.group(2)
        new = datetime.datetime.strptime(date1, '%Y-%m-%d')
        newdate = new.strftime('%a %d of %b')
        time = mo.group(10)
        time = datetime.datetime.strptime(time, '%H:%M')
        time = time + datetime.timedelta(hours=1, minutes=0)
        time = time.strftime('%H:%M')
        return newdate, time


### get the first tranche of data from the getfooty.objAPI class ###

    footyobj = getfooty.objAPI()
    compresult = footyobj.get('competitions/')

### return from class will be resp in variable compresult

    compete = json.loads(compresult.text)


#### populate a table with League names#######
    z = PrettyTable(["Index","League"])
    z.align["League"] = "l"
    index1 = 0
    for i, item in enumerate(compete):
        scrteam = compete[i]['caption']
        index1 += 1
        z.add_row([index1, scrteam])
    print(z)

#### end populate a table ######


#### get user input to identify which league has been chosen #####

    while True:
        usrleague = input('\n\n\nEnter League number\n\n')
        if usrleague.isdigit():
            if int(usrleague) < len(compete)+1:
                break
            else:
                print('Needs to be a lower number')

        else:
            print("Retard!! It needs to be a number")

#### end user input #####


#### get data on teams within chosend league from getfooty.objAPI class ####

    testteams = footyobj.get('competitions/' + str(compete[int(usrleague)-1]['id']) + '/teams')

### parse the returned JSON ####

    allteams = testteams.json()
    teams = allteams['teams']

#### populate a table with team names#######

    y = PrettyTable(["Index","Name"])
    y.align["Name"] = "l"
    index2 = 0
    for i, item in enumerate(teams):
        scrteam = teams[i]['name']
        index2 += 1
        y.add_row([index2, scrteam])

    print(y)

#### end populate table with team names ####

#### get user input to identify which team has been chosen #####

    while True:
        usrteam = input('\n\n\nEnter Team number\n\n')
        if usrteam.isdigit():
            if int(usrteam) < len(teams)+1:
                break
            else:
                print('Needs to be a lower number')

        else:
            print("Retard!! It needs to be a number")

#### end user input #####

### based on user selection find league and team id's from getfooty JSON response ####

    competitionID = compete[int(usrleague)-1]['id']
    teamID = teams[int(usrteam)-1]['id']

#### get data on teams within chosend league from getfooty.objAPI class ####

    fixtures = footyobj.get('competitions/' + str(competitionID) + '/fixtures')

#### parse returned JSON ####

    compfix = fixtures.json()
    compfix2 = compfix['fixtures']

### initialise list that will hold fixture dictionaries for selected team####
    myList = []

### iterate of list to find dictionary key value pairs for selected team.
### when found append these to the myList, list.

    for i, item in enumerate(compfix2):
        if compfix2[i]['homeTeamId'] == teamID:
            myList.append(compfix2[i])
        elif compfix2[i]['awayTeamId'] == teamID:
            myList.append(compfix2[i])


#### populate a table with fixtures#######

    x = PrettyTable(["Home Team", "V", "AwayTeam", "Date","Time"])  #create a table to populate
    x.align["Home Team"]="l"
    x.align["AwayTeam"]="l"

    print('Upcoming Fixtures - \n')


### this loop will discard dictionary items with a key value of status : FINISHED
### all other entries will be added to the table

    for i, item in enumerate(myList):
        finish = (item['status'])
        if finish == 'FINISHED':        #if the status key is FINISHED then ignore
            continue
        else:                           #populate the table with fixtures which do not have a status of FINISHED
            date1 = (item['date'])
            hometeam = (item['homeTeamName'])
            awayteam = (item['awayTeamName'])

            x.add_row([hometeam, "v", awayteam, convertdate(date1)[0],convertdate(date1)[1]])
            x.add_row(["","","","",""])

### end populate table with fixtures ####


    print(x)    #print the PrettyTable


### wait for user input. Either exit program or go back to the start of main()

    while True:
        progcont = input('\n\n Please press C to Continue or E to Exit\n\n')
        progcont = progcont.upper()
        if progcont == 'C':
            #subprocess.call(["printf", "'\033c'"])
            subprocess.call(["reset"])
            main()
        if progcont == 'E':
            sys.exit()


### Get the ball rolling - this is where the program starts

if __name__ == "__main__":
    main()

#TODO: include head to head's
#TODO: include recent results
#TODO: include team values













