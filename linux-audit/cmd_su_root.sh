#!/bin/bash

### send root pwd to execute as root
echo "$2" | sudo -S -u root sh -c "cut -d':' -f1 /etc/passwd | while read id ; do echo -en $1',' &&  passwd -S \$id | sed 's/ /,/g' | tr -d '\012\015' && echo -en ',' &&  lastlog -u \$id | grep -v Latest | awk '{\$1=\"\";printf \"%s\", \$0 }' | sed -e 's/^[ \t]*//' && echo -en ',' &&  chage -l \$id | sed -e 's/.*://' | sed 's/,/ /' | awk '{print}' ORS=',' && echo ''; done;"
