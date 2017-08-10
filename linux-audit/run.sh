#!/bin/bash
if [ $# -lt 1 ]; then
    echo 'Usage: run.sh <password file>'
    exit 0
fi

rm ./output_all.txt
rm ./out/*
declare -i count=0
while read -r line
do
	count=$count+1
	IFS=', ' read -r ip usr upwd rpwd<<< $line
	echo "Processing server "$count
	printf "" > ./out/$ip".res"
	./ssh-connection.sh $ip $usr $upwd $rpwd>> ./out/$ip".res" &
done < "$1"

wait

echo '-Result-' > output_all.txt
cat ./out/*.res >> output_all.txt

echo "Done!"
exit 0

