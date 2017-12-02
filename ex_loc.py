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

# STRUCTURES FOR REGIONS
# -------------------------

# ARRAY OF AREAS
## [[LAT, LONG], [LAT, LONG], ...]

# ARRAY OF NAMES
## [METRO AREA NAME, METRO AREA NAME, ...]

# STRUCTURES FOR BUSINESS FILES
# -------------------------

# ARRAY OF STRINGS
## [STRING OF DATA FOR METRO AREA, STRING OF DATA FOR METRO AREA, ...]
