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


# write = open(sys.argv[2], "w+")
#
# for zips in allzips:
#     cityState = zipdict[zips]
#     for place in cityState:
#         write.write(zips + "\t" + place + "\n")
#
# write.write("LOCATION\tBUS ID\n")
#
# for line in cityLines:
#     write.write(line)

# for line in names:
#     print(line)
