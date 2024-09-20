#!/bin/bash

filename="$1"

grep -o -w '\b[_a-zA-Z][_a-zA-Z0-9]*\b' "$filename" | sort | uniq
