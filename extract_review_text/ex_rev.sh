#!/bin/sh
source_file="$1"
business="$2"
output_dir="$3"
python3 ex_rev.py $source_file $business $output_dir $@
