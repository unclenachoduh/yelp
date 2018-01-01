import sys
import operator # library used to sort dictionary by value
import math # library for log

# -------------------------------------------------------------------
# READ INPUT FILE TO LIST
# -------------------------------------------------------------------
readgram = open(sys.argv[1])
sourcetext = readgram.read()
strings1 = sourcetext.split('\n')
strings = []
# Remove empty lines from list
for line in strings1:
    if line != '':
        strings.append(line)

# -------------------------------------------------------------------
# GET NGRAM PROBS FROM IMPUT FILE
# -------------------------------------------------------------------
# Lists for uni, bi, and trigrams
unigramlist = []
bigramlist = []
trigramlist = []

# ints for token count
unitokencount = 0
bitokencount = 0
tritokencount = 0

# -------------------------------------------------------------------
# SPLIT FILE INTO NGRAM LISTS
# -------------------------------------------------------------------
# Dictionaries for quick search for P(w-i|w-n)
unigramdict = {}
bigramdict = {}

for line in strings:
    splitlines = line.split()

    if len(splitlines) == 2:
        countforline = int(splitlines[0])
        unitokencount += countforline
        unigramlist.append(line)
        if splitlines[1] not in unigramdict:
            unigramdict[splitlines[1]] = countforline
        # else:
        #     print("MULTIPLE OCCURENCE", splitlines[1])

    elif len(splitlines) == 3:
        countforline = int(splitlines[0])
        bitokencount += countforline
        bigramlist.append(line)

        addtodict = splitlines[1] + " " + splitlines[2]
        if addtodict not in unigramdict:
            bigramdict[addtodict] = countforline
        # else:
        #     print("MULTIPLE OCCURENCE", addtodict)
    elif len(splitlines) == 4:
        # print("LENGTH 4")
        countforline = int(splitlines[0])
        tritokencount += countforline
        trigramlist.append(line)
    # else:
    #     print("WRONG LENGTH")


# -------------------------------------------------------------------
# CALCULATE PROBABILITIES (PROB AND LOGPROB)
# -------------------------------------------------------------------
# lists of strings for writeout
unireadytoprint = []
bireadytoprint = []
trireadytoprint = []

def probfunct(line, totcount):
    splitlines = line.split()
    countint = int(splitlines[0])
    shortstr = ""
# get words for output in one string
    for chunk in splitlines[1:]:
        shortstr += chunk + " "

# calc prob and logprob
    indvprob = countint / totcount
    indvlogprob = math.log10(indvprob)

# Formatting to match example
    if indvprob == 0.0:
        indvprob = 0
    elif indvprob == 1.0:
        indvprob = 1
    if indvlogprob == 0.0:
        indvlogprob = 0
    elif indvlogprob == 1.0:
        indvlogprob = 1

    return splitlines[0] + " " + str(indvprob) + " " + str(indvlogprob) + " " + shortstr

for line in unigramlist:
    totcount = unitokencount
    buildstr = probfunct(line, totcount)
    unireadytoprint.append(buildstr)

for line in bigramlist:
    splitlines = line.split()

    findstr = splitlines[1]

    totcount = unigramdict[findstr]

# Do not add words when w-1 does not exist
    if totcount != 0:
        buildstr = probfunct(line, totcount)
        bireadytoprint.append(buildstr)

for line in trigramlist:
    splitlines = line.split()

    findstr = splitlines[1] + " " + splitlines[2]

    totcount = bigramdict[findstr]

# Do not add words if w-1 w-2 does not exist
    if totcount != 0:
        buildstr = probfunct(line, totcount)
        trireadytoprint.append(buildstr)


# -------------------------------------------------------------------
# Output to output file as arg or to stdout
# -------------------------------------------------------------------
output_str = "THIS IS GENERIC OUTPUT BECAUSE THERE IS NO OUTPUT ARG"
output_file = None # If there's no output file given, use standard out.
if len(sys.argv) > 2:
    output_file = sys.argv[2]

if output_file is not None:
    writeme = open(output_file, "w+")

    writeme.write("\\data\\\n")
    writeme.write("ngram 1: type=" + str(len(unigramlist)) + " token=" + str(unitokencount) + "\n")
    writeme.write("ngram 2: type=" + str(len(bigramlist)) + " token=" + str(bitokencount) + "\n")
    writeme.write("ngram 3: type=" + str(len(trigramlist)) + " token=" + str(tritokencount) + "\n")
    writeme.write("\n\\1-grams:\n")
    for uniline in unireadytoprint:
        writeme.write(uniline + "\n")
    writeme.write("\n\\2-grams:\n")
    for biline in bireadytoprint:
        writeme.write(biline + "\n")
    writeme.write("\n\\3-grams:\n")
    for triline in trireadytoprint:
        writeme.write(triline + "\n")
    writeme.write("\n\\end\\")
else:
    print("\\data\\\n")
    print("ngram 1: type=" + str(len(unigramlist)) + " token=" + str(unitokencount) + "\n")
    print("ngram 2: type=" + str(len(bigramlist)) + " token=" + str(bitokencount) + "\n")
    print("ngram 3: type=" + str(len(trigramlist)) + " token=" + str(tritokencount) + "\n")
    print("\n\\1-grams:\n")
    for uniline in unireadytoprint:
        print(uniline + "\n")
    print("\n\\2-grams:\n")
    for biline in bireadytoprint:
        print(biline + "\n")
    print("\n\\3-grams:\n")
    for triline in trireadytoprint:
        print(triline + "\n")
    print("\n\\end\\")
