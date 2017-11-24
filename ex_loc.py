import sys
import re

# --------------------------------------
# IMPORT REFERENCE FILES
# --------------------------------------

# --------------------------------------
# SOURCE FILE
readSource = open(sys.argv[1])
sourceText = readSource.read()
sourceText = re.sub("[{}]", "", sourceText)
sourceLines = sourceText.split("\n")

# # ZIP CODE FILE
# readZIP = open(sys.argv[3])
# ZIPText = readZIP.read()
# ZIPLines = ZIPText.split("\n")

# COORDINATES FILE
readCOORD = open(sys.argv[4])
COORDText = readCOORD.read()
COORDLines = COORDText.split("\n")

print("READ FILES")


# # --------------------------------------
# # CREATE ZIP CODE DICTIONARY
# # --------------------------------------
#
# # Dictionary for zip codes : 'city, state'
# zipdict = {}
# # List of zip codes
# allzips = []
# # List of all State names
# allstatenames = []
#
# # BUILD ZIP CODE DICTIONARY
# for line in ZIPLines:
#     if line != '':
#         parts = line.split(",")
#
#         zipcode = str(parts[0])
#         cityname = parts[1]
#         stateabbrv = parts[3]
#
#         if zipcode not in zipdict:
#             zipdict[zipcode] = [cityname + ", " + stateabbrv]
#             allzips.append(zipcode)
#         else:
#             zipdict[zipcode].append(cityname + ", " + stateabbrv)
#
#         if stateabbrv not in allstatenames:
#             allstatenames.append(stateabbrv)
#
#
# print("BUILD ZIP DICT")


# --------------------------------------
# CREATE COORDINATES DICTIONARY
# --------------------------------------

# Dictionary for metro areas name : index
coorddict = {}
# List of zip codes
allcoords = []
# List of lat ranges
lats = []
# list of longi ranges
longi = []
# List of all State names
metronames = []
# LATITUDE OR LONGITUDE VALUES STATE MANAGER
values = ""



# BUILD ZIP CODE DICTIONARY
for line in COORDLines:
    if line != '':
        if line[0] == "/":
            values = line
        else:
            parts = line.split("\t")

            metro = str(parts[0])
            low = float(parts[1])
            high = float(parts[2])

            if values == "/coordinates":
                coorddict[metro] = len(metronames)
                metronames.append(metro)
            elif values == "/latitude":
                index = coorddict[metro]
                lats[index] = [low, high]
            elif values == "/longitude":
                index = coorddict[metro]
                longi[index] = [low, high]

            while len(lats) < len(metronames):
                lats.append(None)
                longi.append(None)


print("BUILD COORD DICT")

count = 0

for name in metronames:
    print(name, lats[count], longi[count])
    count += 1



# --------------------------------------
# BUSINESS LOCATIONS
# --------------------------------------

# array of strings to be printed to each FILE
printme = [[]] * len(metronames)

# String for printing business with no area
noarea = []

# string for printing businesses with more than one area
morearea = []

for line in sourceLines:
    if line != '':

# Split Json line into valuable data chunks
        line = re.sub("\": \"", "\t", line)
        parts = line.split("\", \"")
        secondparts = parts[7].split(",")
        count = 0

        idParts = parts[0].split("\t")
        nameParts = parts[1].split("\t")
        cityParts = parts[4].split("\t")
        stateParts = parts[5].split("\t")
        postalParts = parts[6].split("\t")
        latparts = secondparts[0].split(": ")
        longparts = secondparts[1].split(": ")

        # for part in parts:
        #     print(part)
# Useful Location Variables from Json Line
        business_id = idParts[1]
        # name
        # neighborhood
        # address
        city = cityParts[1]
        # state
        # postal_code
        latitude = float(latparts[1])
        longitude = float(longparts[1])

        printstring = business_id + "\t" + city + "\t" + str(latitude) + "\t" + str(longitude)

        areacount = 0
        for name in metronames:
            index = coorddict[name]

            print(name, index)

            if latitude > lats[index][0] and latitude < lats[index][1] and longitude > longi[index][0] and longitude > longi[index][1]:
                printme[index].append(printstring + "\n")
                print("WINNER", name, printstring)
                areacount += 1

        if areacount == 0:
            noarea.append(printstring + "\n")
        elif areacount > 1:
            morearea.append(printstring + "\n")

        # print(business_id, city, latitude, longitude)


print("BUILD BUSINESS DICT")




# --------------------------------------
# PRINT SHOP
# --------------------------------------

printcount = 0

for target in printme:
    writefile = open("AREABUS/METRO_" + metronames[printcount], "w+")
    print(target, "TARG")
    for line in target:
        if line != '':
            writefile.write(line)
            print(line, "LINE IN TARG")
    printcount += 1

writefile = open("AREABUS/METRO_NO_AREA", "w+")
for line in noarea:
    writefile.write(line)
    print(line, "NO")

writefile = open("AREABUS/METRO_MORE_AREA", "w+")
for line in morearea:
    writefile.write(line)
    print(line, "MORE")
