# author = UncleNachoDuh
# ex_rev.py
# ---------------------------------------------------------------------------
# This file reads the review file from the Yelp dataset (10) and creates
# A file comtaining review data for all reviews that fall within
# the latitude/longitude region for each metro area defined in the AREAS file
# ---------------------------------------------------------------------------

import sys
import os
import numpy as np
import operator

input_dir = sys.argv[1]
business_file = sys.argv[2]
output_dir = sys.argv[3]

if input_dir[:-1] != "/":
    input_dir += "/"

if output_dir[:-1] != "/":
    output_dir += "/"

# --------------------------------------------------
# PROCESS BUSINESS FILE
# --------------------------------------------------

# -------------------------
# DATA STRUCTURES FOR REGIONS
# -------------------------

# ARRAY OF DICTIONARIES FOR BUSINESS IDs
big_business = []

# SORTED ARRAY OF ALL BUSINESS IDs
bigger_business = {}
bigger_arr = []

# ARRAY OF REGION NAMES
region_names_arr = []

# DICTIONARY OF REGION NAMES
region_names = {}

# -------------------------
# READ BUSINESS FILE
# -------------------------

business_read = open(business_file)
business_text = business_read.read()
business_lines = business_text.split("\n")

section = "PROBLEM"

for line in business_lines:
    if line != '':
        if "/" in line:
            section = line[1:]
            region_names[section] = len(region_names_arr)

            region_names_arr.append(section)
            big_business.append({})
            # print(len(big_business))
        else:
            big_business[len(big_business)-1][line] = section
            bigger_business[line] = section


bigger_arr = sorted(sorted(bigger_business.items(), key=operator.itemgetter(0)))
count = 0
# while count < 101:
#     print(bigger_arr[count])
#     count += 1

ids = []
regs = []

for pair in bigger_arr:
    ids.append(pair[0])
    regs.append(pair[1])



# print("FINISHED: BUSINESS FILE")
# -------------------------
# CHECK REGION DATA STRUCTURES
# -------------------------

# writefile = open(output_dir + "CHECK_REG", "w+")
#
# count = 0
# for d in big_business:
#     sort = sorted(d.items(), key=operator.itemgetter(1))
#
#     writefile.write("/" + region_names_arr[count] + "\n")
#
#     for x in sort:
#         writefile.write(x[0] + "\n")
#
#     writefile.write("\n")
#
#     count += 1
# writefile.close()

# count = 0
# for reg in region_names_arr:
#     print(reg, count)
#     count += 1


# --------------------------------------------------
# PROCESS REVIEWS FILE
# --------------------------------------------------

# -------------------------
# DATA STRUCTURES FOR REVIEWS
# -------------------------

# ARRAY OF REVIEWS STRINGS
reviews = [''] * len(region_names_arr)
qa_reviews = [''] * len(region_names_arr)

# print("LENGTH REG NAMES", len(region_names_arr))

# ARRAY OF SOURCE FILES
source_files = sorted(os.listdir(input_dir))

# -------------------------
# READ REVIEWS FILE
# -------------------------
#
# input_read = open(input_file)
# input_text = input_read.readlines()
# input_lines = input_text.split("\n")

# count = 0
# for line in reviews:
#     print(count)
#     count += 1
#     print("\n")

for filename in source_files:
    print(filename)

    name_parts = filename.split("_")
    file_num = name_parts[1]

    input_read = open(input_dir + filename)
    input_text = input_read.read()
    input_read.close()
    input_lines = input_text.split("\n")

    count = 0
    for line in input_lines:
        if line != '':
            if count % 25000 == 0:
                # num = str(int(count / 250000))
                print(count, "/", len(input_lines) - 1)
            count += 1

            line_parts = line.split("\",\"")

            id_parts = line_parts[2].split("\":\"")
            bus_id = id_parts[1]
            text_parts = line_parts[4].split("\":\"")
            text = text_parts[1]

            # print("-----\n" + bus_id + "\n" + text + "\n-----\n")

            find = np.searchsorted(ids, bus_id)

            if ids[find] == bus_id:

                index = region_names[regs[find]]
                # print(index)
                reviews[index] += text + "\n"
                qa_reviews[index] += bus_id + "\t" + text + "\n"

    count = 0

    for string in reviews:
        # print(string)
        # print(count, len(reviews))
        # # print(string[:50])
        # print(region_names_arr[count])
        if string != '':
            print("write", region_names_arr[count])
            writefile = open(output_dir + region_names_arr[count] + "_" + file_num, "w+")
            writefile.write(string)
            writefile.close()

            writefile = open(output_dir + "QA_" + region_names_arr[count] + "_" + file_num, "w+")
            writefile.write(qa_reviews[count])
            writefile.close()
            # print("STRING", string)
            # print(string)

        count += 1














print("\n# -------------------------\n  FINISHED\n# -------------------------\n")
