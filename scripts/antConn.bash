#!/bin/bash

# year month day hour min 

out=$(curl -s -u void:password 192.168.131.135:1936 | grep "conn rate" | awk '{print $12}' | sed 's/[^0-9]*//g')

date=$(date +%Y%m%d%H%M)

echo $date $out



