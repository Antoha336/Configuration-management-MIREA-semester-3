#!/bin/bash

input_file=$1
output_file=$2

touch $output_file
cat $input_file | sed "s/    /\t/g" > $output_file
