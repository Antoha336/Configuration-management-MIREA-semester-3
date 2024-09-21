#!/bin/bash

filename="$1"
line=$(head -n 1 "$filename").c

if [[ $filename =~ \.(c)$ ]]; then
  if [[ $line =~ ^(\/\/) ]]; then
    echo "$filename has a comment"
  else
    echo "$filename doesn't have a comment"
  fi
elif [[ $filename =~ \.(js)$ ]]; then
  if [[ $line =~ ^(\/\*) ]]; then
    echo "$filename has a comment"
  else
    echo "$filename doesn't have a comment"
  fi
elif [[ $filename =~ \.(py)$ ]]; then
  if [[ $line =~ ^(\#) ]]; then
    echo "$filename has a comment"
  else
    echo "$filename doesn't have a comment"
  fi
else
  echo "$filename doesn't have a comment"
fi
