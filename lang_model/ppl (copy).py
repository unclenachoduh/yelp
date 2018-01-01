import sys
import operator # library used to sort dictionary by value
import math # library for log

# print(sys.argv[1]) # lm_file
# print(sys.argv[2]) # L1
# print(sys.argv[3]) # L2
# print(sys.argv[4]) # L3
# print(sys.argv[5]) # test_data
# print(sys.argv[6]) # output_file

# -------------------------------------------------------------------
# READ INPUT FILE TO LIST
# -------------------------------------------------------------------
readdata = open(sys.argv[5])
sourcetext = readdata.read()
strings1 = sourcetext.split('\n')
strings = []
# Remove empty lines from list
for line in strings1:
    addtotestarraytemp = "<s> " + line + " </s>"
    if line != '':
        strings.append(addtotestarraytemp)
        # print(addtotestarraytemp)

    # print(addtotestarraytemp)

# -------------------------------------------------------------------
# READ LANG MODEL FILE TO DICTS
# -------------------------------------------------------------------
# Dictionaries for ngrams
unigramdict = {}
bigramdict = {}
trigramdict = {}

totalunigrams = 0
totalbigrams = 0
totaltrigrams = 0

readlm = open(sys.argv[1])
lmtext = readlm.read()
lmstrings1 = lmtext.split('\n')
lmstrings = []

# LOOP BELOW ENSURES
# Remove empty lines from list
# Non LM data is not included

whichdict = 0

for line in lmstrings1:
    thingsinline = line.split()
    gramname = ""
    for word in thingsinline[3:]:
        gramname += word + " "
    gramname = gramname[:-1]

    if line != '':
        if thingsinline[0] == "ngram":
            tempsplit = thingsinline[3].split("=")
            if thingsinline[1] == "1:":
                totalunigrams = int(tempsplit[1])
            if thingsinline[1] == "2:":
                totalbigrams = int(tempsplit[1])
            if thingsinline[1] == "3:":
                totaltrigrams = int(tempsplit[1])

    if line == "\\1-grams:":
        whichdict = 1
        # print("1gram")
    elif line == "\\2-grams:":
        whichdict = 2
        # print("2gram")
    elif line == "\\3-grams:":
        whichdict = 3
        # print("3gram")
    elif line != '' and line != "\\end\\" and whichdict > 0:

        if whichdict == 1:
            unigramdict[gramname] = thingsinline
        elif whichdict == 2:
            bigramdict[gramname] = thingsinline
        elif whichdict == 3:
            trigramdict[gramname] = thingsinline

# -------------------------------------------------------------------
# CALCULATE PERPLEXITY
# -------------------------------------------------------------------
# Array for lines to print
arrayforprint = []

def tracen1(phrase):
    if phrase in bigramdict:
        return True
    else:
        return False

def tracen12(phrase):
    if phrase in trigramdict:
        return True
    else:
        return False

def trace12(phrase):
    if phrase in bigramdict:
        return True
    else:
        return False

def tracen(phrase):
    if phrase in unigramdict:
        return True
    else:
        return False

def trace1(phrase):
    if phrase in unigramdict:
        return True
    else:
        return False

def trace2(phrase):
    if phrase in unigramdict:
        return True
    else:
        return False


# Function for calculating perplexity
def perplexity(wordn, wordn2, wordn1, checkn, check1, check2, checkn1, checkn12, check12, needed):

    lam1 = float(sys.argv[2])
    lam2 = float(sys.argv[3])
    lam3 = float(sys.argv[4])

    probgiven2 = 0
    probgiven1 = 0
    probgiven0 = 0

# wordn
    if checkn == True:
        unithings = unigramdict[wordn]
        unicounts = int(unithings[0])

        probgiven0 = lam1 * (unicounts / totalunigrams)

# wordn1
    if checkn1 == True:

        biphrase = wordn1 + " " + wordn

        bithings = bigramdict[biphrase]
        bicounts = int(bithings[0])

        biunithings = unigramdict[wordn1]
        biunicounts = int(biunithings[0])

        probgiven1 = lam2 * (bicounts / biunicounts)

# wordn2
    if check12 == True and checkn12 == True:
        tribiphrase = wordn2 + " " + wordn1

        tribithings = bigramdict[tribiphrase]
        tribicounts = int(tribithings[0])

        triphrase = tribiphrase + " " + wordn

        trithings = trigramdict[triphrase]
        tricounts = int(trithings[0])

        probgiven2 = lam3 * ( tricounts / tribicounts)

    probabilityofthisword = probgiven2 + probgiven1 + probgiven0

    return probabilityofthisword

totaloovcount = 0
totalwordcount = 0
bigsum = 0
sentencecount = 0
for line in strings:
    words = line.split()

# sum of probabilities of trigrams
    sumprob = 0

# out of vocabulary counter
    oov = 0
    linetoarrayforprint = "\nSent #" + str(sentencecount + 1) + ": " + line

    arrayforprint.append(linetoarrayforprint)

    # print("\n" + line)
    wordcount = 0
    for word in words:

        linetoarrayforprint = str(wordcount) + ": lg P(" + word + " | "

        existbool = False

        if word in unigramdict:
            existbool = True
            # print(word, "IN DICTIONARY")
        else:
            oov += 1
        #     print("WE HAVE A PROBLEM WITH THIS WORD", word)

        if wordcount == 0:
            wordcount += 1
        else:
            if wordcount == 1:
                # calc bigram

                linetoarrayforprint += words[wordcount-1] + ") = "

                thistry = words[wordcount-1] + " " + word
# Check that w_1... exists
                prebool1 = trace1(words[wordcount-1])
# Check that w1 w2 exists
                prebooln1 = tracen1(thistry)

                if existbool == True:
                    perp = perplexity(word, "no", words[wordcount-1], existbool, prebool1, False, prebooln1, False, False, 1)
                    logperp = math.log10(perp)
                    linetoarrayforprint += str(logperp)
                    sumprob += logperp
                else:
                    linetoarrayforprint += "-inf (unknown word)"

                if (prebooln1 == False or prebool1 == False) and existbool == True:
                    linetoarrayforprint += " (unseen ngrams)"

                arrayforprint.append(linetoarrayforprint)

                # print("Bigram", words[wordcount-1], word)
            # elif counter < len(words) - 1:
            else:
                # calc trigram

                preworkout = words[wordcount-2] + " " + words[wordcount-1]
                thistry = words[wordcount-1] + " " + word
                tricheck = preworkout + " " + word
#check that w1 w2 w3 exists
                prebool3 = False
                if tricheck in trigramdict:
                    prebool3 = True

# Check that w_1 exists
                prebool1 = trace1(words[wordcount-1])
# Check that w_2 exists
                prebool2 = trace2(words[wordcount-2])
# Check that w_1 w_2 exist
                prebool12 = trace12(preworkout)
#check that w1 w2 w3 exist
                prebooln12 = tracen12(tricheck)
# Check that w1 w2 exists
                prebooln1 = tracen1(thistry)


                linetoarrayforprint += preworkout + ") = "

                if existbool == True:
                    perp = perplexity(word, words[wordcount-2], words[wordcount-1], existbool, prebool1, prebool2, prebooln1, prebool12, prebooln12, 2)

                    logperp = math.log10(perp)
                    linetoarrayforprint += str(logperp)
                    sumprob += logperp
                else:
                    linetoarrayforprint += "-inf (unknown word)"

                if (not prebool1 or not prebool2 or not prebooln1 or not prebool12 or not prebooln12) and existbool == True:
                    linetoarrayforprint += " (unseen ngrams)"

                arrayforprint.append(linetoarrayforprint)

                # print("TRIGRAM", words[wordcount-2], words[wordcount-1], word)

            wordcount += 1



    lgprob = sumprob
    total = lgprob / (wordcount -2 + 1 - oov)
    totalperp = 10**-total
    arrayforprint.append("1 sentence, " + str(len(words) - 2) + " words, " + str(oov) + " OOVs")
    arrayforprint.append("lgprob=" + str(lgprob) + " ppl=" + str(totalperp) + "\n\n")
    sentencecount += 1
    totalwordcount += wordcount -2
    bigsum += sumprob
    totaloovcount += oov

# -------------------------------------------------------------------
# TOTALS FOR FILE
# -------------------------------------------------------------------
arrayforprint.append("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
arrayforprint.append("sent_num=" + str(sentencecount) + " word_num=" + str(totalwordcount) + " oov_num=" + str(totaloovcount))

finalline = "lgprob=" + str(bigsum)

avglgprob  = bigsum / (totalwordcount + sentencecount - totaloovcount)

finalppl = 10**-avglgprob

finalline += " ave_lgprob=" + str(avglgprob)
finalline += " ppl=" + str(finalppl)
arrayforprint.append(finalline)



# -------------------------------------------------------------------
# WRITE OR PRINT
# -------------------------------------------------------------------
# lists of strings for writeout
unireadytoprint = sorted(unigramdict.items(), key=operator.itemgetter(1), reverse=True)
bireadytoprint = sorted(bigramdict.items(), key=operator.itemgetter(1), reverse=True)
trireadytoprint = sorted(trigramdict.items(), key=operator.itemgetter(1), reverse=True)

# print(unireadytoprint[0])
# print(bireadytoprint[0])
# print(trireadytoprint[0])

# print("COUNTS:\n", totalunigrams, "\n", totalbigrams, "\n", totaltrigrams, "\n")

output_str = "THIS IS GENERIC OUTPUT BECAUSE THERE IS NO OUTPUT ARG"
output_file = None # If there's no output file given, use standard out.
if len(sys.argv) > 6:
    output_file = sys.argv[6]

if output_file is not None:
    writeme = open(output_file, "w+")

    for eachline in arrayforprint:
        writeme.write(eachline + "\n")
else:
    for eachline in arrayforprint:
        print(eachline)
































# </python>
