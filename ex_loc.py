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

# ZIP CODE FILE
readZIP = open(sys.argv[3])
ZIPText = readZIP.read()
ZIPLines = ZIPText.split("\n")


print("READ FILES")


# --------------------------------------
# CREATE ZIP CODE DICTIONARY
# --------------------------------------

# Dictionary for zip codes : 'city, state'
zipdict = {}
# List of zip codes
allzips = []
# List of all State names
allstatenames = []

# BUILD ZIP CODE DICTIONARY
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

        if stateabbrv not in allstatenames:
            allstatenames.append(stateabbrv)


print("BUILD ZIP DICT")



# --------------------------------------
# BUSINESS LOCATIONS
# --------------------------------------

cities = {}
cityLines = []
names = []
states = {}
statenames = []

usastates = []
notstates = []


for line in sourceLines:
    if line != '':
        line = re.sub("\": \"", "\t", line)
        parts = line.split("\", \"")
        count = 0
        # while count < 7:
        #     print(count, parts[count])
        #     count += 1

        cityParts = parts[4].split("\t")
        stateParts = parts[5].split("\t")
        idParts = parts[0].split("\t")
        postalParts = parts[6].split("\t")


        loc = cityParts[1] + ", " + stateParts[1]
        # if loc not in cities:
        #     cities[loc] = len(cityLines)
        #     cityLines.append("\n" + loc + "\t" + idParts[1] + "\n")
        #     # names.append(loc)
        # else:
        #     cityLines[cities[loc]] += loc + "\t" + idParts[1] + "\n"

        if stateParts[1] not in allstatenames:
            if stateParts[1] not in notstates:
                states[stateParts[1]] = [cityParts[1] + "\t" + idParts[1]]
                notstates.append(stateParts[1])
            else:
                states[stateParts[1]].append(cityParts[1] + "\t" + idParts[1])
        else:
            if stateParts[1] not in usastates:
                states[stateParts[1]] = [cityParts[1] + "\t" + idParts[1]]
                usastates.append(stateParts[1])
            else:
                states[stateParts[1]].append(cityParts[1] + "\t" + idParts[1])

        if stateParts[1] not in statenames:
            statenames.append(stateParts[1])


print("BUILD BUSINESS DICT")




# --------------------------------------
# PRINT SHOP
# --------------------------------------


# write = open(sys.argv[2], "w+")

for name in usastates:
    print(name)

    write = open(sys.argv[2] + "/USA/LOCS_" + name, "w+")
    cityNames = states[name]
    for place in cityNames:
        write.write(name + "\t" + place + "\n")

for name in notstates:
    print(name)

    write = open(sys.argv[2] + "/NOT/LOCS_" + name, "w+")
    cityNames = states[name]
    for place in cityNames:
        write.write(name + "\t" + place + "\n")
#
# write.write("LOCATION\tBUS ID\n")
#
# for line in cityLines:
#     write.write(line)

# for line in names:
#     print(line)
