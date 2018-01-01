import sys
import operator # library used to sort dictionary by value

# -------------------------------------------------------------------
# READ INPUT FILE TO LIST
# -------------------------------------------------------------------
readtrain = open(sys.argv[1])
sourcetext = readtrain.read()
strings1 = sourcetext.split('\n')
strings = []
# Remove empty lines from list
for line in strings1:
    if line != '':
        strings.append(line)

# -------------------------------------------------------------------
# COUNT GRAMS FROM IMPUT FILE
# -------------------------------------------------------------------
# Dictionaries for uni, bi, and trigrams
unigramdict = {}
bigramdict = {}
trigramdict = {}

for i in strings:
# add BOS and EOS
    i = "<s> " + i + " </s>"

    words = i.split()

    gramcounter = 0
    for word in words:
# add every word to unigram dictionary or update count
        if word not in unigramdict:
            unigramdict[word] = 1
        else:
            unigramdict[word] += 1

# If penultimate word, add w and w+1 to bigram dictionary
        if len(words) > gramcounter + 1:
            bigramstr = word + " " + words[gramcounter + 1]

            if bigramstr not in bigramdict:
                bigramdict[bigramstr] = 1
            else:
                bigramdict[bigramstr] += 1

# If antepenultimate word, add w and w+1 to trigram dictionary
        if len(words) > gramcounter + 2:
            trigramstr = word + " " + words[gramcounter + 1] + " " + words[gramcounter + 2]

            if trigramstr not in trigramdict:
                trigramdict[trigramstr] = 1
            else:
                trigramdict[trigramstr] += 1

        gramcounter += 1

# -------------------------------------------------------------------
# Lists for each ngram dictionary, sorted by count
# -------------------------------------------------------------------
unireadytoprint = sorted(unigramdict.items(), key=operator.itemgetter(1), reverse=True)
bireadytoprint = sorted(bigramdict.items(), key=operator.itemgetter(1), reverse=True)
trireadytoprint = sorted(trigramdict.items(), key=operator.itemgetter(1), reverse=True)

# -------------------------------------------------------------------
# Output to output file as arg or to stdout
# -------------------------------------------------------------------
output_str = "THIS IS GENERIC OUTPUT BECAUSE THERE IS NO OUTPUT ARG"
output_file = None # If there's no output file given, use standard out.
if len(sys.argv) > 2:
    output_file = sys.argv[2]

if output_file is not None:
    writeme = open(output_file, "w+")

    for uniline in unireadytoprint:
        writeme.write(str(uniline[1]) + "\t" + uniline[0] + "\n")
    for biline in bireadytoprint:
        writeme.write(str(biline[1]) + "\t" + biline[0] + "\n")
    for triline in trireadytoprint:
        writeme.write(str(triline[1]) + "\t" + triline[0] + "\n")
else:
    for uniline in unireadytoprint:
        writeme.write(str(uniline[1]) + "\t" + uniline[0] + "\n")
    for biline in bireadytoprint:
        writeme.write(str(biline[1]) + "\t" + biline[0] + "\n")
    for triline in trireadytoprint:
        writeme.write(str(triline[1]) + "\t" + triline[0] + "\n")
