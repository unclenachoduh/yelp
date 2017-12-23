#!/bin/sh
source_file="$1"
output_file="$2"
postal_codes="$3"
python3 ex_loc.py $source_file $output_file $postal_codes $@
