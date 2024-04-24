#!/bin/bash
source ~/anaconda3/etc/profile.d/conda.sh
filename="/home/cmpuser1/naoqi/pepper_mod2/pepper_text.json"


while true; do
    echo -e "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    # Read the first character from the file
    if ! head -c 1 "$filename" | grep -q '[^[:space:]]'; then
        echo -e "\n$filename is empty, skipping GPT...\n"

    else
        echo -e "\nRunning GPT..."
        python march_gpt.py

        # Activate Conda environment
        conda activate pepper

        # Run the Pepper Feedback script
        python pepper_feedback.py

        # Deactivate Conda environment
        conda deactivate
    #uncomment client_websoc and fix IP for IoT
        #python client_websoc.py
    fi
    # Empty the pepper_text.json file
    echo -n > "$filename"
    sleep 1  # Add a delay to avoid continuous checking
done
