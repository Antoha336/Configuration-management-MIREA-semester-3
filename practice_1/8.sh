#!/bin/bash

directory=$1
ext=$2

mkdir -p ./temp
find "$directory" -type f -name "*.$ext" -exec cp {} ./temp +
tar -cf "${ext}_files.tar" ./temp
rm -R ./temp
