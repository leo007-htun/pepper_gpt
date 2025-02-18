#!/bin/bash
source ~/anaconda3/etc/profile.d/conda.sh
filename="/home/cmpuser1/pepper_gpt/pepper_text.json"


while true; do
    echo -e "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    # Read the first character from the file
    if ! head -c 1 "$filename" | grep -q '[^[:space:]]'; then
        echo -e "\n$filename is empty, skipping GPT...\n" 

    elif grep -q "take" "$filename" && grep -q "picture" "$filename"; then
        echo -e "\n$filename contains 'take' and 'picture', skipping GPT...\n"

    elif grep -q "play" "$filename"; then
        echo -e "\n$filename contains 'take' and 'picture', skipping GPT...\n"
        #python music.py

        #conda activate pepper

        #python tablet.py

        #conda deactivate
    elif grep -q "dance" "$filename"; then
        echo -e "\n$filename contains 'dance', skipping GPT...\n"
    else

    	conda activate

        echo -e "\nRunning GPT..."
        python march_gpt.py

        # Activate Conda environment
        conda activate pepper

        # Run the Pepper Feedback script
        python pepper_feedback.py

        # Deactivate Conda environment
        conda deactivate

        #uncomment client_websoc and fix IP for IoT ==> both IoT device and Pepper must be under same LAN
        #python client_websoc.py
    
    fi
    # Empty the pepper_text.json file
    echo -n > "$filename"
    sleep 1  # Add a delay to avoid continuous checking
done
<< COMMENT

#!/bin/bash
source ~/anaconda3/etc/profile.d/conda.sh
filename="/home/cmpuser1/pepper_gpt/pepper_text.json"

while true; do
    echo -e "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    # Read the first character from the file
    if ! head -c 1 "$filename" | grep -q '[^[:space:]]'; then
        echo -e "\n$filename is empty, skipping GPT...\n"
    else
        # Check if the file contains the phrase "take picture"
        if grep -q "take picture\|cheese\|chease" "$filename"; then
            echo -e "\nFound 'take picture' in the file, skipping GPT..."
	    sleep 10
 
        else
            echo -e "\nRunning GPT..."
            python march_gpt.py

            # Activate Conda environment
            conda activate pepper

            # Run the Pepper Feedback script
            python pepper_feedback.py

            # Deactivate Conda environment
            conda deactivate
        fi

        #uncomment client_websoc and fix IP for IoT ==> both IoT device and Pepper must be under same LAN
        #python client_websoc.py
    fi
    # Empty the pepper_text.json file
    echo -n > "$filename"
    sleep 1  # Add a delay to avoid continuous checking
done




#!/bin/bash
source ~/anaconda3/etc/profile.d/conda.sh
filename="/home/cmpuser1/pepper_gpt/pepper_text.json"


while true; do
    echo -e "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    # Read the first character from the file
    if ! head -c 1 "$filename" | grep -q '[^[:space:]]'; then
        echo -e "\n$filename is empty, skipping GPT...\n"


    else
        if grep -iq 'dance' "$filename"; then
            echo -e "\nDancing..."  

        else

            echo -e "\nRunning GPT..."
            python march_gpt.py

            # Activate Conda environment
            conda activate pepper

            # Run the Pepper Feedback script
            python pepper_feedback.py

            # Deactivate Conda environment
            conda deactivate

            #uncomment client_websoc and fix IP for IoT ==> both IoT device and Pepper must be under same LAN
            #python client_websoc.py
        fi
    fi
    # Empty the pepper_text.json file
    echo -n > "$filename"
    sleep 1  # Add a delay to avoid continuous checking
done

#UNCOMMENT BELOW FOR WAKE-WORD "HEY PEPPER"


#!/bin/bash
source ~/anaconda3/etc/profile.d/conda.sh
filename="/home/cmpuser1/pepper_gpt/pepper_text.json"

while true; do
    echo -e "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    # Read the first character from the file
    if ! head -c 1 "$filename" | grep -q '[^[:space:]]'; then
        echo -e "\n$filename is empty, skipping GPT...\n"
    else
        # Check if the file contains the required words
        if ! grep -iq 'pepper\|papa\|papper\|peppa\|pappa' "$filename"; then
            echo -e "\nWake-Word not Detected, skipping GPT...\n"
        else
            echo -e "\nRunning GPT..."
            python march_gpt.py

            # Activate Conda environment
            conda activate pepper

            # Run the Pepper Feedback script
            python pepper_feedback.py

            # Deactivate Conda environment
            conda deactivate
        fi
    fi
    # Empty the pepper_text.json file
    echo -n > "$filename"
    sleep 1  # Add a delay to avoid continuous checking
done



#!/bin/bash
source ~/anaconda3/etc/profile.d/conda.sh
filename="/home/cmpuser1/pepper_gpt/pepper_text.json"

# Function to read the JSON file
read_json_file() {
    while true; do
        if grep -q "stop" "$filename"; then
            echo "Detected 'stop' in the JSON file. Skipping the main script tasks."
                # Skip the main script tasks
            continue
        fi
    done
}

# Start the JSON file reading process in the background
read_json_file &

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
COMMENT
