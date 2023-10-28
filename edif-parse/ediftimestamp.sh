#!/bin/sh
#This script accepts the name of an EDIF file and modifies that timestamp within the file to be that of the file's mtime.
#Atmel's ATF150X CPLD fitters have quotes in the timestamp, which makes it unparseable to Spydrnet.
#Finally, this restores the file's original mtime to what it was before the script was run.
date -r "$1"
MTIME=`date -r "$1" "+%Y %m %d %H %M %S"`
echo "Adjusting timestamp in file: $1"
sed -i "s/(timeStamp\".*\")/(timeStamp ${MTIME})/" "$1"

MTIME=`echo $MTIME | sed 's/\(....\) \(..\)\ \(..\)\ \(..\)\ \(..\)\ \(..\)/\1\2\3\4\5.\6/'` #Convert to a format that touch wants
touch -t $MTIME "$1" #Restore files original modification time