# author = UncleNachoDuh

# -------------------------------------------------------
# Merge all files within a given folder
# -------------------------------------------------------
# merge.py

import sys
import os

# ------------------
# ARGUMENTS
# ------------------

thresh = 200000

source_dir =sys.argv[1]
targ_dir = sys.argv[2]

if source_dir[-1] != "/":
    source_dir += "/"
if targ_dir[-1] != "/":
    targ_dir += "/"

source_files = sorted(os.listdir(source_dir))

# file_counter = 0

for name in source_files:
    if name != "COMBINE":
        print(name)

        local_files = sorted(os.listdir(source_dir + name))
        writefile = open(targ_dir + "TRAIN/" + name, "w+")
        writefile2 = open(targ_dir + "TEST/" + name, "w+")
        # file_counter += 1
        count = 0

        for local in local_files:
            if count < thresh:
                print(local)

                readme = open(source_dir + name + "/" + local)
                text = readme.readlines()

                local_count = 0
                while count < thresh and local_count < len(text):
                    if count % 10 == 0:
                        writefile2.write(text[local_count])
                    else:
                        writefile.write(text[local_count])
                    local_count += 1
                    count += 1


        print(count)
        writefile.close()
