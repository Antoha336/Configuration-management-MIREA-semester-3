#!/bin/bash

directory="$1"

hash=$(find "$directory" -type f -exec md5sum {} + | sort | uniq -w 32 -d | awk '{print $1}')
find "$directory" -type f -exec md5sum {} + | grep "$hash" | awk '{print $2}'
