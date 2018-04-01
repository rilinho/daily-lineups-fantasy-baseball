#my current roster in FAAB
my_players = [
    "Travis d'Arnaud",
    "Josh Bell",
    "Paul DeJong",
    "Freddie Freeman",
    "Ketel Marte",
    "José Martínez",
    "Rhys Hoskins",
    "Christian Yelich",
    "Domingo Santana",
    "Lorenzo Cain",
    "Scott Kingery",
    "Javier Báez",
    "Orlando Arcia",
    "José Pirela ",    
]


import requests

from bs4 import BeautifulSoup

url = 'http://dailybaseballdata.com/cgi-bin/dailyhit.pl?date=&xyear=0&pa=1&showdfs=&sort=ops&r40=2&scsv=1&nohead=1&noskip=1'
r = requests.get(url)
r_html = r.text

soup = BeautifulSoup(r_html)

#splits eveything by semicolon, since we can't use commas, which are in the names
raw_data = soup.string.split(';')

#makes everything a string
raw_data = [str(x) for x in raw_data]

#takes out the header
header = raw_data[2:49]

#isolates the data from the header and extra crap
data = raw_data[49:]

#gives us the length of the header which we will use to define the size of the groups we will need to split the data
interval = len(header)

#splits up the data by the size of the header
players_data = [data[x:x+interval] for x in xrange(0, len(data), interval)]

#takes out an extra character for a line break that is generated
players_data.pop(-1)

#makes a list of the players names
players = [x[3] for x in players_data]

#makes a dictionary with the list of player names and their corresponding data set
players_dict = dict(zip(players,players_data))

#the indice of the stats we want to get from each entry of players_data
stats_index = [6,17,18,19,22,24,25,27,29,31,32,33,34,-8,-6]

def recommendation(name,menu,stats):
    
    #making it easier to calculate conditions with stats
    PA = float(stats["PA"])
    AB = float(stats["AB"])
    BB = float(stats["BB"])
    Hits = float(stats["Hits"])
    HR = float(stats["HR"])
    SB = float(stats["SB"])
    RBI = float(stats["RBI"])
    AVG = float(stats["AVG"])
    OBP = float(stats["OBP"])
    Pitcher = str(stats["Pitcher_name(FL)"])
    Throws = str(stats["Throws"])
    
    if AVG > 0.300 or OBP > 0.250 or HR > 2 or SB > 2:
        print "--> START against %s (%s)" % (Pitcher,Throws)
    else:
        print "--> SIT against %s (%s)" % (Pitcher,Throws)
    
    

#pull out the key and value for the player_dict dictionary
for (x,y) in players_dict.items():
    
    # if there is a hit from the my_players list
    if x in my_players:
        
        #set a variable name with the name
        name = x
        
        #set an empty list for the menu which we will populate
        menu = []
        
        #set an empty list for the stats which we will populate
        stats = []
        
        #for each element in the stats_index list, which are really indicies...
        for i in stats_index:
            #add on the corresponding item at the indice from the "y" which is stats_index wrapped up in a dict
            stats.append(y[i])
            #add on the corresponding item from the header menu
            menu.append(header[i])
        
        #zip the newly created menu and stats lists together in a dictionary
        stats = dict(zip(menu,stats))
        
        print "%s (%s)" % (name,str(stats["Bats"]))
        recommendation(name,menu,stats)
        print stats
        print "\n"
        
