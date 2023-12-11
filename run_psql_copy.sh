#!/bin/bash
sdir="/data/CP2/ftp/af/"
pid=`ps -ef | grep -v grep | grep "file_handler.py" | wc -l`
file=`ls -ltr ${sdir}|grep "^-"|awk '{print $NF}'`
fileNum=`ls -ltr ${sdir}|grep "^-"|awk '{print $NF}' | wc -l`
count=0
if [ ${pid} -eq 0 ]
then
	for i in ${file}
	do
		last_time=$(stat -c %Y ${sdir}${i})
		current_time=$(date +%s)
		timediff=$((${current_time}-${last_time}))
		if [ $timediff -gt 600 ]
		then
			count=$((${count}+1))
		fi
	done
	if [ ${count} = ${fileNum} ]
	then
		source /etc/profile
		cd /data/CP2/app/whitelist_copy_to_cpdb_af/
		/usr/local/bin/python3 /data/CP2/app/whitelist_copy_to_cpdb_af/py/file_handler.py /data/CP2/app/whitelist_copy_to_cpdb_af/conf/table_mappings.csv /data/CP2/ftp/af/
	fi
else
	exit 2
fi
#python3 py/file_handler.py conf/table_mappings.csv /data/CP2/ftp/af/
