import socket
import openai
from collections import Counter

api_key = 'your API key'
openai.api_key = api_key
#HOST = '192.168.8.137'    # Pepper's IP
HOST = 'localhost'  
PORT = 4567                # The same port as used by the server
global rev_lst
rev_lst = []
res_lst = []

def chat_with_assistant(user_input):

    response = openai.ChatCompletion.create(
        #model="gpt-3.5-turbo-0613",
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "you are a humanoid pepper robot from Liverpool JohnMoores University. You work for TALASCM project by helping Seniors and older adults in their daily lives. try to answer briefly as possible. Try to be funny. remove numbers when you answer and put spaces after each sentence or puntuations."},
            {"role": "user", "content": user_input},
        ],

        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    assistant_response = response['choices'][0]['message']['content']
    print("\nAssistant:", assistant_response)
    return assistant_response

if __name__ == "__main__":
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            data = s.recv(1024)
            output_string = data.decode("utf-8")
                    
            print('Received :',type(output_string), output_string)
            rev_lst.append(output_string)
            print('received list: ', rev_lst)

            # If rev_lst contains more than two elements, remove the first element
            if len(rev_lst) > 1:
                rev_lst = rev_lst[-1:]
                print('Received List Final:', rev_lst)
            print('Received List Final1:', rev_lst)

            str_rev = ' '.join(rev_lst)    
            with open("pepper_text.txt", "w") as file:
                file.write(str_rev)

'''# Receive data from the server

            # TODO remove '[]' and convert completely into str
            # Receive data once
        
            data = s.recv(1024)


            output_string = data.decode("utf-8")
                
            print('Received :',type(output_string), output_string)

            #data = ""

            #rev_lst.append(output_string)
            #removed_overlapped_list = remove_overlapping_words(rev_lst)
            #rev_lst.append(removed_overlapped_list)
            #print('received list: ', rev_lst)

            #rev_lst = [] receives twice (loop twice) DO not use

            # Call the chat_with_assistant function with the received data as input
            

            if not data:  # If received data is empty, indicating end of transmission
                print("Empty data ... closing socket")
                #pass
                break
            
            # Print the received data
            #print('Received:', user_input)
            #chat_with_assistant(user_input)'''

