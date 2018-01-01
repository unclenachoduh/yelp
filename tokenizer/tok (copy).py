
import re
import sys

def spaces(word):
    seq = ""
    count = 0
    for c in word:
        if re.match("\W", c):
            c = " " + c + " "
        seq += c
    return seq

# Get and create list of abbreviations
abbrvPath = sys.argv[1]
abbrvSource = open(abbrvPath)
abbrvText = abbrvSource.read()
abbrvList = abbrvText.split("\n")

# Get thet source text
source_dir = sys.argv[2]
source = open(source_dir)
sourceText = source.readlines()
# sourceList = sourceText.split("\n")

file_name = source_dir
if "/" in file_name:
    parts = file_name.split("/")
    file_name = parts[-1]

target_dir = sys.argv[3]
if target_dir[-1] != "/":
    target_dir += "/"

target = open(target_dir + file_name, "w+")

count = 0
for line in sourceText:

    count += 1
    ten_per = int(len(sourceText)/10)
    one_per = int(len(sourceText)/100)
    # if count % ten_per == 0:
    if count % ten_per == 0:
        print(count, len(sourceText))

    toPrint = ""
    # if "\\n" in line:
    #     print("BLAND", line)
    line = re.sub(r"\\[n/\"]", "", line)
    # print("AFTER", line)

    words = line.split()
    # print(line)

    for word in words:

        if re.match(r"^.*[\W].*$", word):

            seq = spaces(word)

            # Allow abbreviations
            for abbrv in abbrvList:
                fake = spaces(abbrv)
                if re.match("^.*" + fake + ".*$", seq):
                    seq = re.sub(fake, abbrv, seq)

            if re.match("^.* (\w \. )+.*$", seq):
                seq = re.sub(" \. ", ".", seq)

            # Allow Email
            if re.match("^.*[\S]+ @ [\S]+ \. [\S]+.*$", seq):
                seq = re.sub(" \. ", ".", seq)
                seq = re.sub(" @ ", "@", seq)
                seq = re.sub("(\s@\s|\s@|@\s|@$|^@)", " @ ", seq)
                seq = re.sub("(\s\.\s|\s\.|\.\s|\.$|^\.)", " . ", seq)

            # Allow URLs
            if re.match("^.* : .* / .* \. .*$", seq):
                seq = re.sub(" \. ", ".", seq)
                seq = re.sub(" / ", "/", seq)
                seq = re.sub(" : ", ":", seq)

                #seq = re.sub("/", " / ", seq)
                seq = re.sub("(:\s|\s:)", " : ", seq)
                seq = re.sub("(\s\.\s|\s\.|\.\s|\.$|^\.)", " . ", seq)

            # Allow Paths
            if re.match("^.*:?.*\\.*$", seq):
                seq = re.sub(r" \\ ", r"\\", seq)
                seq = re.sub(" : ", ":", seq)
                seq = re.sub("(: | :|:$|^:)", " : ", seq)

            if re.match("^.*[ ~ ]?[ : ]? / .*$", seq):
                seq = re.sub(" ~ ", "~", seq)
                seq = re.sub(" / ", "/", seq)
                seq = re.sub("( : | :|: )", ":", seq)
                seq = re.sub("(: | :|:$|^:)", " : ", seq)

            # Allow Numbers
            if re.match("^.*\d{1,3}( , \d{3})*( \. \d*)?.*$", seq):
                # allow period for decimal
                seq = re.sub(" \. ", ".", seq)
                if re.match("^((\.|(\D\.\D|\D\.|\.\D))|\.)$", seq):
                    seq = re.sub(".", " . ", seq)
                # allow comma for thousands
                # currently allows bad number format for improper English
                seq = re.sub(" , ", ",", seq)
                if re.match("^((.*|(\D,\D|\D,|,\D|,$)|,).*)$", seq):
                    seq = re.sub(",", " , ", seq)
                # allow dash for minus
                seq = re.sub(" - ", "-", seq)
                if re.match("^.*((\D-\D|\D-|-\D).*|-)$", seq):
                    seq = re.sub("-", " - ", seq)

            # Allow fractions
            if re.match("^.*\d+ / \d+.*$", seq):
                seq = re.sub(" / ", "/", seq)
                if re.match("^((/)|(\D/\D|\D/|/\D))|(/))$", seq):
                    seq = re.sub("/", " / ", seq)

            # Allow Dash
            if re.match("^.* -  - .*$", seq):
                seq = re.sub(" -  - ", " -- ", seq)

            # Allow ellipsis
            if re.match("^.* \.  \.  \. .*$", seq):
                seq = re.sub(" \.  \.  \. ", " ... ", seq)

            # Allow percentage
            seq = re.sub(" % ", "%", seq)

            # Allow contractions
            seq = re.sub("n ' t", " n't ", seq)
            seq = re.sub(" ' ve", " 've ", seq)
            seq = re.sub(" ' ll", " 'll ", seq)
            seq = re.sub(" ' m", " 'm ", seq)
            seq = re.sub(" ' d", " 'd ", seq)
            seq = re.sub(" ' re", " 're ", seq)
            seq = re.sub(" ' s", " 's ", seq)
            seq = re.sub(" ' all", " 'all ", seq)

            seq = re.sub("o ' clock", "o'clock", seq)
            seq = re.sub("s ' ", "s'", seq)

            word = seq

            # if "\\n" in word:
            #     print(word)
            # word = re.sub("\\n", "", word)
            # print(word)

        toPrint += word + " "

    toPrint = re.sub(" +", " ", toPrint)
    target.write(toPrint + "\n")
