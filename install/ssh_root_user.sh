#!/bin/bash
USER_NAME="root"
HOST_FILE="/home/weka/hosts"
ERROR_FILE="/home/weka/ssh-copy_error.txt"
PUBLIC_KEY_FILE="$1"

if [ ! -f  $PUBLIC_KEY_FILE ]; then
        echo "File '$PUBLIC_KEY_FILE' not found!"
        exit 1
fi

if [ ! -f $HOST_FILE ]; then
        echo "File '$HOST_FILE' not found!"
        exit 2
fi

for IP in `cat $HOST_FILE`; do
        ssh-copy-id -i $PUBLIC_KEY_FILE $USER_NAME@$IP 2>$ERROR_FILE
        RESULT=$?
        if [ $RESULT -eq 0 ]; then
                echo ""
                echo "Public key successfully copied to $IP"
                echo ""
        else
                echo "$(cat  $ERROR_FILE)"
                echo 
                exit 3
        fi
        echo ""
done
