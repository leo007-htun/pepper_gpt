import openai
import os
import json

api_key = ''
openai.api_key = api_key
input_file_path = "/home/cmpuser1/pepper_gpt/pepper_text.json"  # Replace with the actual path to your text file
output_file_path = "/home/cmpuser1/pepper_gpt/response.txt"  # Replace with the desired output file path

'''def detect_words(file_path, target_words):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                for word in target_words:
                    if word in line:
                        return True
        return False
    
    except Exception as e:
        print("Error:", e)
        return False

def read_and_delete_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            print("Contents of the JSON file:", data)
        
        # Delete the content of the file
        with open(file_path, 'w') as file:
            file.truncate(0)
        
        print("Content of the JSON file has been deleted.")
    
    except FileNotFoundError:
        print("File not found at the specified path.")
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
    except Exception as e:
        print("An error occurred:", e)

def is_blank(content):
    # Check if the content is empty or contains only whitespace characters
    return not content.strip()

def overwrite_with_blank(file_path):
    try:
        # Overwrite the file with blank content
        with open(file_path, "w") as file:
            file.write("")
        print("File {} overwritten with blank content.".format(file_path))
    except Exception as e:
        print("Error overwriting file with blank content:", str(e))'''

def chat_with_assistant(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        data = json.load(file)
        print("Contents of the JSON file:", data)

    response = openai.ChatCompletion.create(
        #model="gpt-3.5-turbo-0613",
        #model="gpt-3.5-turbo-1106",
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "you are a humanoid pepper robot from Liverpool JohnMoores University. You work for TALASCM project by helping Seniors and older adults in their daily lives. try to answer briefly as possible. You do have the ability to take pictures with your cameras. two arms to show gestures and sensors to avoid obstacles. You would like to shake hands but your motors have stiffness which will damage them. Remove emojis when you reply. And you can definitely dance and play music. IF someone ask 'Can you dance?', just say you can and do not ask anything back. When someone ask you to play music, play jingle bell.Plus you have installed tic-tac-toe game, if someone ask for games to play."},
            {"role": "user", "content": data},
        ],

        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    assistant_response = response['choices'][0]['message']['content']
    print("\nAssistant:", assistant_response)



    # Save the assistant's response to the output file
    with open(output_file_path, "w") as output_file:
        output_file.write(assistant_response)
            # Delete the content of the file
    #with open(input_file_path, 'w') as file:
        #file.truncate(0)

if __name__ == "__main__":
    '''target_words = ["pepper", "hello", "hi"]  # List of words to detect'''
    chat_with_assistant(input_file_path, output_file_path)
