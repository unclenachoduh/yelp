#!/bin/sh
source_file="$1"
output_file="$2"
python3 ex_post.py $source_file $output_file $@
