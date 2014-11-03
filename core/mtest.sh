#!/bin/bash


# backups.sh
badge="Unknow"
name="Unknow"
position="Unknow"
usage()
{
        echo "Usage: `basename $0` -d [device] -l [logfile] -q"
        exit 1
}
while getopts b:n:p: OPTION
do
        case $OPTION in
                b) badge=$OPTARG
                ;;
                n) name=$OPTARG
                ;;
                p) position=$OPTARG
                ;;
                \?) usage
                ;;
        esac
done
echo "*******************"
echo "badge"
echo "$badge"
echo "name" 
echo "$name"
echo "position" 
echo "$position"
