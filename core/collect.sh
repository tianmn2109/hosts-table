#!/bin/bash

my_version="%(version)s"
delimiter="%(delimiter)s"
collect_url="%(collect_url)s"
version_url="%(version_url)s"
upload_url="%(upload_url)s"
arguments=$@

badge="Unknow"
name="Unknow"
position="Unknow"
usage()
{
        echo "Usage:  -b [badgenumber] -n [name] -p [machineposition]"
        exit 1
}

check_version() {
    server_version=$(curl -s "$version_url")
    if [ "$server_version" != "$my_version" ]; then
        echo "Version mismatch, my($my_version), server($server_version). Please fetch $collect_url for update !"
        exit 1
    fi
}

        #echo "name"
       # echo "$name" 
        #echo "$delimiter"

        #echo "badge"
        #echo "$badge" 
        #echo "$delimiter"

        #echo "position"
        #echo "$position" 
        #echo "$delimiter"

upload() {
    export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:$PATH
    (
        echo "hostname"
        hostname
        echo "$delimiter"

        echo "df"
        sudo df -lT -x tmpfs -x devtmpfs -B G
        echo "$delimiter"
   
        echo "mac"
        sudo ifconfig | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'
        echo "$delimiter"
        
        echo "args"
        echo "$arguments"
        echo "$delimiter"

        echo "osinfo"
        sudo uname -rop
        echo "$delimiter"
 
        
        echo "dmidecode"
        sudo dmidecode
        echo
    ) | curl -X POST --data-binary @- "$upload_url"
}

args(){
    while getopts b:n:p: OPTION
    do
        case $OPTION in
            b)badge=$OPTARG
                ;;
            n)name=$OPTARG
                ;;
            p)position=$OPTARG
                ;;
         esac
    done
}
#### Main
check_args(){
    if [ ! -n "$arguments" ] ; then
        arguments="name=Unknow;position=Unknow;badge=Unknow"
    fi
}
check_version
#args
check_args
upload
