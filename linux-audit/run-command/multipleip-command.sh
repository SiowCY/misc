#!/bin/sh
#password=$1
command=$1
file="ip-user-pass.txt"
while IFS="," read ip username password; do
	echo $ip
	sshpass -p$password ssh -t -q -o StrictHostKeyChecking=no $username@$ip "$command" &
	sleep 1

done < $file
