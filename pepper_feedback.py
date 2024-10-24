'''import qi
import os

def read_aloud(text_to_read, session):
    tts = session.service("ALTextToSpeech")
    tts.setLanguage("English")  # Adjust language if necessary
    tts.say(text_to_read)

def delete_txt_files(directory_path):
    try:
        # List all files in the specified directory
        files = os.listdir(directory_path)

        # Iterate through the files and delete if the file has a .txt extension
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(directory_path, file)
                os.remove(file_path)
                print("Deleted: {}".format(file_path))

        print("Deletion completed.")
    except Exception as e:
        print("Error: {}".format(e))

if __name__ == "__main__":
    session = qi.Session()
    session.connect("tcp://10.42.0.239:9559")  # Replace with Pepper's IP and port

    # Replace the following line with the actual path to your text file
    text_file_path = "/home/leo/pynaoqi/response.txt"

    with open(text_file_path, 'r') as file:
        text_to_read = file.read()

    # Read the text aloud using ALTextToSpeech
    read_aloud(text_to_read, session)
    delete_txt_files(text_file_path)
'''
import qi
import os
import time

def get_robot_ip_from_file(file_path):
    # Open the text file in read mode
    with open(file_path, 'r') as file:
        # Read the IP address from the file and strip newline characters
        ip_addresses = file.readline().strip()
    return ip_addresses

def read_aloud(text_to_read, session):
    ttsa = session.service("ALAnimatedSpeech")
    tts = session.service("ALTextToSpeech")
    audio = session.service("ALAudioDevice")
    tts.setVolume(1.0)
    tts.setParameter("speed", 90)
    configuration = {"bodyLanguageMode":"contextual"}
    audio.unsubscribe("SpeechRecognition")
    ttsa.say(text_to_read,configuration)
    audio.subscribe("SpeechRecognition")


def delete_txt_file(file_path):
    try:
        # Check if the file exists before attempting to delete
        if os.path.exists(file_path):
            os.remove(file_path)
            print("Deleted: {}".format(file_path))
        else:
            print("File does not exist: {}".format(file_path))

    except Exception as e:
        print("Error: {}".format(e))


if __name__ == "__main__":
    # Replace 'ip_addresses' with the path to your IP file
    ip_file_path = "ip.txt"
    robot_ip = get_robot_ip_from_file(ip_file_path)
    session = qi.Session()
    session.connect("tcp://{}:9559".format(robot_ip))

    # Replace the following line with the actual path to your text file
    text_file_path = "/home/cmpuser1/pepper_gpt/response.txt"

    with open(text_file_path, 'r') as file:
        text_to_read = file.read()

    if os.path.isfile(text_file_path) and os.path.getsize(text_file_path) > 0:
        with open(text_file_path, 'r') as file:
            text_to_read = file.read()
        # Read the text aloud using ALTextToSpeech
        
        read_aloud(text_to_read, session)

    # Delete the text file
    else:
        print("No Text file!!!")

    delete_txt_file(text_file_path)
