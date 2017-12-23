#!/bin/sh
source_file="$1"
coord="$2"
blacklist="$3"
output_dir="$4"
python3 ex_loc.py $source_file $coord $blacklist $output_dir $@
