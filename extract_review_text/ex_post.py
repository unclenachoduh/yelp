##
# Separate the yelp data by postal code
##

import sys
import re

readZIP = open(sys.argv[1])
ZIPText = readZIP.read()
ZIPLines = ZIPText.split("\n")

zipdict = {}
allzips = []


for line in ZIPLines:
    if line != '':
        parts = line.split(",")

        zipcode = str(parts[0])
        cityname = parts[1]
        stateabbrv = parts[3]


        if zipcode not in zipdict:
            zipdict[zipcode] = [cityname + ", " + stateabbrv]
            allzips.append(zipcode)
        else:
            zipdict[zipcode].append(cityname + ", " + stateabbrv)
