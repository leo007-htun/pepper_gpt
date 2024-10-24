#!/bin/bash
source ~/anaconda3/etc/profile.d/conda.sh
filename="/home/cmpuser1/naoqi/pepper_mod2/response.txt"  # Add the response file path

while true; do
    echo -e "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    # Read the first character from the file
    if ! head -c 1 "$filename" | grep -q '[^[:space:]]'; then
        echo -e "\n$filename is empty, skipping response...\n"
    else
        echo -e "\nRunning feedback..."
        python pepper_feedback.py
    fi
    sleep 1  # Add a delay to avoid continuous checking
done
