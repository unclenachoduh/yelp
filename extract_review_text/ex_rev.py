# author = UncleNachoDuh
# ex_rev.py
# ---------------------------------------------------------------------------
# This file reads the review file from the Yelp dataset (10) and creates
# A file comtaining review data for all reviews that fall within
# the latitude/longitude region for each metro area defined in the AREAS file
# ---------------------------------------------------------------------------

import sys
import os
# import re
# import operator

input_dir = sys.argv[1]
business_file = sys.argv[2]
output_dir = sys.argv[3]

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
        else:
            big_business[len(big_business)-1][line] = section


print("FINISHED: BUSINESS FILE")
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


# --------------------------------------------------
# PROCESS REVIEWS FILE
# --------------------------------------------------

# -------------------------
# DATA STRUCTURES FOR REVIEWS
# -------------------------

# ARRAY OF REVIEWS STRINGS
reviews = [''] * len(big_business)
qa_reviews = reviews

# ARRAY OF SOURCE FILES
source_files = sorted(os.listdir(input_dir))

# -------------------------
# READ REVIEWS FILE
# -------------------------
#
# input_read = open(input_file)
# input_text = input_read.readlines()
# input_lines = input_text.split("\n")



for filename in source_files:
    print(filename)


count = 0
# for line in input_text:
#     if line != '':
#         if count % 10000 == 0:
#             # num = str(int(count / 250000))
#             print(count, "/", len(input_text))
#         count += 1
#
#         line_parts = line.split("\",\"")
#
#         id_parts = line_parts[2].split("\":\"")
#         bus_id = id_parts[1]
#         text_parts = line_parts[4].split("\":\"")
#         text = text_parts[1]
#
#         # print("-----\n" + bus_id + "\n" + text + "\n-----\n")
#
#         for reg in big_business:
#             if bus_id in reg:
#                 reg_name = reg[bus_id]
#
#                 index = region_names[reg_name]
#
#                 reviews[index] += text + "\n"
#                 qa_reviews += bus_id + "\t" + text + "\n"

print("FINISHED: REVIEWS")

count = 0
#
# for string in reviews:
#
#     writefile = open(output_dir + region_names_arr[count], "w+")
#     writefile.write(string)
#     writefile.close()
#
#     writefile = open(output_dir + "QA_" + region_names_arr[count], "w+")
#     writefile.write(qa_reviews[count])
#     writefile.close()
#
#     count += 1














print("# -------------------------\n  FINISHED\n# -------------------------\n")
