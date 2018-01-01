#!/bin/sh
ngram_count_file="$1"
lm_file="$2"
python3 build_lm.py $ngram_count_file $lm_file $@
