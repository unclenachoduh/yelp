# author = UncleNachoDuh
# ex_loc.py
# ---------------------------------------------------------------------------
# This file reads the business file from the Yelp dataset (10) and creates
# A file comtaining business data for all businesses that fall within
# the latitude/longitude region for each metro area defined in the AREAS file
# ---------------------------------------------------------------------------

import sys

input_file_loc = sys.argv[1]
areas_file_loc = sys.argv[2]
output_dir = sys.argv[3]


# --------------------------------------------------
# DATA STRUCTURES
# --------------------------------------------------

# -------------------------
# STRUCTURES FOR REGIONS
# -------------------------

# ARRAY OF AREAS LAT VALUES
## [[NORTH LAT, SOUTH LAT], [NORTH LAT, SOUTH LAT], ...]
area_lats = []

# ARRAY OF AREAS LONG VALUES
## [[NORTH LONG, SOUTH LONG], [NORTH LONG, SOUTH LONG], ...]
area_longs = []

# ARRAY OF NAMES
## [METRO AREA NAME, METRO AREA NAME, ...]
area_names_arr = []
area_names = {}

# -------------------------
# STRUCTURES FOR BUSINESS FILES
# -------------------------

# ARRAY OF STRINGS
## [STRING OF DATA FOR METRO AREA, STRING OF DATA FOR METRO AREA, ...]
all_strings = []

# --------------------------------------------------
# READ AREAS FILE
# --------------------------------------------------

areas_file = open(areas_file_loc)
areas_text = areas_file.read()
areas_lines = areas_text.split("\n")

section = "/coordinates"
name_index = 0

for area_line in areas_lines:
    parts = area_line.split("\t")
    if len(parts) < 3:
        section = area_line
    else:
        if section == "/coordinates":
            area_names_arr.append(parts[0])
            area_names[parts[0]] = name_index
            name_index += 1
            area_lats.append([[],[]])
            area_longs.append([[],[]])
        elif section == "/latitude":
            area_lats[area_names[parts[0]]] = [float(parts[1]),float(parts[2])]
        elif section == "/longitude":
            area_longs[area_names[parts[0]]] = [float(parts[1]),float(parts[2])]

# -------------------------
# CHECK AREA DATA STRUCTURES
# -------------------------

# print("\nNAMES")
# x = 0
# for line in area_names_arr:
#     print(line, area_names[line])
#     x += 1
# print("\nLATS")
# for line in area_lats:
#     print(line)
# print("\nLONGS")
# for line in area_longs:
#     print(line)

# --------------------------------------------------
# PRINT SHOP
# --------------------------------------------------

print("\n# -------------------------\n  Yeah, Baby, Yeah!\n# -------------------------\n")
