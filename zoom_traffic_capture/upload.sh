#!/bin/bash
# $1 is the folder where files to upload are
# $2 folder name
for f in $1/*
do
	if [ $f = $1"/uploads/*" ]
	then
	    continue
	fi
	
	if ! [[ `lsof $f` ]]
	then
	    
	    # Upload the file to google drive
	    echo "Attempting to upload $f"	
	    sudo /root/.google-drive-upload/bin/gupload $f -r -C $2 && rm -f $f
	fi
done
