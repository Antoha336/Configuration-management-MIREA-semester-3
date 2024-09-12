#!/bin/bash

message="$1"
length=${#message}

border="+-"
for (( i=0; i<length; i++ )); do
  border="${border}-"
done
border="${border}-+"

echo "$border"
echo "| $message |"
echo "$border"
