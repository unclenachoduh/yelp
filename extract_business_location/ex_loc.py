# author = UncleNachoDuh
# ex_loc.py
# ---------------------------------------------------------------------------
# This file reads the business file from the Yelp dataset (10) and creates
# A file comtaining business data for all businesses that fall within
# the latitude/longitude region for each metro area defined in the AREAS file
# ---------------------------------------------------------------------------

import sys
import re

input_file_loc = sys.argv[1]
areas_file_loc = sys.argv[2]
output_dir = sys.argv[3]

if output_dir[-1] != "/":
    output_dir += "/"

# --------------------------------------------------
# PROCESS AREAS FILE
# --------------------------------------------------

# -------------------------
# DATA STRUCTURES FOR REGIONS
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
# READ AREAS FILE
# -------------------------

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

print("\nNAMES\tLATS\tLONGS\n")
x = 0
for line in area_names_arr:
    print(line, area_names[line], area_lats[x], area_longs[x])
    x += 1

print("\n")

# --------------------------------------------------
# PROCESS INPUT FILE
# --------------------------------------------------

# -------------------------
# DATA STRUCTURES FOR BUSINESS FILES
# -------------------------

# ARRAY OF STRINGS
## [STRING OF DATA FOR METRO AREA, STRING OF DATA FOR METRO AREA, ...]
all_strings = [''] * (len(area_names_arr) + 2)

# STRING FOR SPREADSHEET
spread = 'BUS_ID\tLONG\tLAT\n'

# ARRAY FOR SPREADSHEET
spreads = [''] * (len(area_names_arr) + 2)

# ARRAY FOR ALL POINTS SPREADSHEET
all_spreads = [''] * 4


# -------------------------
# READ BUSINESS FILE
# -------------------------

input_file = open(input_file_loc)
input_text = input_file.read()
input_lines = input_text.split("\n")

for line in input_lines:
    if line != '':
        line = re.sub("\": ", "\t", line)
        line = re.sub("\": \"", "\t", line)
        parts = line.split("\", \"")

        cityParts = parts[4].split("\t\"")
        stateParts = parts[5].split("\t\"")
        idParts = parts[0].split("\t\"")
        postalParts = parts[6].split("\t\"")

        line_id = idParts[1]
        # print(line_id)

        loc = cityParts[1] + ", " + stateParts[1]

        geo_parts = parts[7].split(", ")

        latparts = geo_parts[0].split("\t")
        lonparts = geo_parts[1].split("\t")

        if latparts[1] != "null" and lonparts[1] != "null":
            line_lat = float(latparts[1])
            line_lon = float(lonparts[1])

            # print(loc, line_lat, line_lon)
            # print(idParts[1], line_lat, line_lon)

            # THIS ARRAY WRITES ALL BUSINESSES TO FILES

            if line_lat > 0:
                if line_lon > -20:
                    all_spreads[0] += str(line_lat) + "\t" + str(line_lon) + "\n"
                else:
                    all_spreads[1] += str(line_lat) + "\t" + str(line_lon) + "\n"
            else:
                if line_lon > -20:
                    all_spreads[2] += str(line_lat) + "\t" + str(line_lon) + "\n"
                else:
                    all_spreads[3] += str(line_lat) + "\t" + str(line_lon) + "\n"

            send_line = line_id + "\n"

            one_check = False
            more_check = False

            area_count = 0

            double_saver = []
            for line in area_lats:
                # print("LATS: ", area_lats[area_count][0], area_lats[area_count][1])
                if line_lat > area_lats[area_count][0] and line_lat < area_lats[area_count][1]:
                    # print("LONGS: ", area_longs[area_count][0], area_longs[area_count][1])
                    if line_lon > area_longs[area_count][0] and line_lon < area_longs[area_count][1]:
                        all_strings[area_count] += send_line
                        spreads[area_count] += line_id + "\t" + str(line_lon) + "\t" + str(line_lat) + "\n"
                        spread += line_id + "\t" + str(line_lon) + "\t" + str(line_lat) + "\n"
                        # print("SUCCESS")
                        if one_check == True:
                            more_check = True
                        one_check = True
                        double_saver.append(area_names_arr[area_count])
                # print("AC: ", area_count)
                area_count += 1

            if one_check == False:
                all_strings[len(all_strings)-2] += send_line

            if more_check == True:
                all_strings[len(all_strings)-1] += send_line

            if len(double_saver) > 1:
                print(send_line, double_saver)

        else:
            all_strings[len(all_strings)-2] += send_line


# -------------------------
# CHECK BUSINESS DATA STRUCTURES
# -------------------------

# count = 0
# print("ALL STRINGS")
# for line in all_strings:
#     name = "DUBS"
#     if count < len(area_names_arr) - 1:
#         name = area_names_arr[count].upper()
#     if count == len(area_names_arr):
#         name = "MISSING"
#     print(str(count) + " ---- " + name + "\n" + line)
#     count += 1

# --------------------------------------------------
# PRINT SHOP
# --------------------------------------------------

finalfile = open(output_dir + "04_BUSINESSES", "w+")

print_count = 0
for line in all_strings:
    name = "03_DUPLICATES"
    if print_count < len(area_names_arr):
        name = area_names_arr[print_count].upper()
    if print_count == len(area_names_arr):
        name = "03_OUTLIER"

    writefile = open(output_dir + name, "w+")
    writefile.write(line)
    writefile.close()

    if name != "03_DUPLICATES" and name != "03_OUTLIER":
        finalfile.write("/" + name + "\n" + line + "\n")

    # print(name)

    print_count += 1

finalfile.close()


writefile = open(output_dir + "02_ACC_GLOB", "w+")
writefile.write(spread)
writefile.close()


writefile = open(output_dir + "02_ACC_US", "w+")
counter = 0
writefile.write('BUS_ID\tLONG\tLAT\n')
while counter < 9:
    writefile.write(spreads[counter])
    # print("USA PLOT: ", counter)
    counter += 1


writefile.close()


writefile = open(output_dir + "02_ACC_BA", "w+")
writefile.write('BUS_ID\tLONG\tLAT\n')
writefile.write(spreads[counter])
writefile.close()
# print("BA PLOT: ", counter)
counter += 1

writefile = open(output_dir + "02_ACC_EU", "w+")
writefile.write('BUS_ID\tLONG\tLAT\n')
while counter < 13:
    writefile.write(spreads[counter])
    # print("EU PLOT: ", counter)
    counter += 1


writefile.close()


writefile = open(output_dir + "01_QUAD_NE", "w+")
writefile.write(all_spreads[0])
writefile.close()
writefile = open(output_dir + "01_QUAD_NW", "w+")
writefile.write(all_spreads[1])
writefile.close()
writefile = open(output_dir + "01_QUAD_SE", "w+")
writefile.write(all_spreads[2])
writefile.close()
writefile = open(output_dir + "01_QUAD_SW", "w+")
writefile.write(all_spreads[3])
writefile.close()

print("# -------------------------\n  FINISHED\n# -------------------------\n")
