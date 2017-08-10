#!/bin/sh
ip=$1
password=$2
command=$3
sshpass -p$password ssh -o StrictHostKeyChecking=no root@$ip "$command" &
