#!/bin/sh
#password=$1
command=$1
file="ip-user-pass.txt"
while IFS="," read ip password; do
	echo $ip
	ssh -o StrictHostKeyChecking=no -o ConnectTimeout=1 root@$ip &
	sleep 1
done < $file
