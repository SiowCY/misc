#!/bin/bash

if [ $# -lt 3 ]; then
	echo $requirement
	echo " "
	echo $usage
	echo " "
	echo $example
else
	ip=$1
	user=$2
	upass=$3
	rpass=$4

	if [ $# -lt 4 ]; then
		#execute as sudoer or root
		sshpass -p $upass ssh -o "StrictHostKeyChecking=no" $user@$ip "bash -s" < ./cmd_sudo "$ip" &
	else
		#execute as normal user and switch to root
		sshpass -p $upass ssh -o "StrictHostKeyChecking=no" $user@$ip "bash -s" < ./cmd_su_root "$ip" "$rpass" &
	fi
	wait
fi
exit 0
