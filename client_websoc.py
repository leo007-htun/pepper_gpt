#https://shawnhymel.com/1675/arduino-websocket-server-using-an-esp32/
#https://www.youtube.com/watch?v=ZbX-l1Dl4N4

'''import websocket

# Connect to WebSocket server
ws = websocket.WebSocket()
ws.connect("ws://10.84.220.14") #copy IP from esp32 monitor
print("Connected to WebSocket server")

# Ask the user for some input and transmit it
#str = input("Say something: ")
ws.send("turnoff_led")

# Wait for server to respond and print it
result = ws.recv()
print("Received: " + result)

# Gracefully close WebSocket connection
ws.close()
'

import websocket

# Connect to WebSocket server
ws = websocket.WebSocket()
ws.connect("ws://192.168.8.136") # Copy IP from ESP32 monitor
print("Connected to WebSocket server")

# Read the content of the .txt file
with open('pepper_text.txt', 'r') as file:
    file_content = file.read()

# Check if the file contains the word "switch on"
if "switch on" in file_content:
    # Send "lit_led" to the WebSocket server
    ws.send("lit_led")
    print("Sent: lit_led")

elif "switch off" in file_content:
    # Send "lit_led" to the WebSocket server
    ws.send("turnoff_led")
    print("Sent: turnoff_led")

else:
    print("No 'switch on' found in the file.")

# Gracefully close WebSocket connection
ws.close()

import websocket

# Define WebSocket event handlers
def on_open(ws):
    print("Connected to WebSocket server")

def on_message(ws, message):
    print("Received:", message)

def on_close(ws):
    print("WebSocket connection closed")

# Connect to WebSocket server and set event handlers
ws = websocket.WebSocketApp("ws://192.168.8.136",
                            on_open=on_open,
                            on_message=on_message,
                            on_close=on_close)

# Read the content of the .txt file
with open('pepper_text.txt', 'r') as file:
    file_content = file.read()

# Check if the file contains the word "switch on"
if "switch on" in file_content:
    # Send "lit_led" to the WebSocket server
    ws.send("lit_led")
    print("Sent: lit_led")

elif "switch off" in file_content:
    # Send "lit_led" to the WebSocket server
    ws.send("turnoff_led")
    print("Sent: turnoff_led")

else:
    print("No 'switch on' found in the file.")

# Run the WebSocket event loop
ws.run_forever()
'''
import websocket
import json

# Connect to WebSocket server
ws = websocket.create_connection("ws://192.168.8.136")  # Copy IP from ESP32 monitor
print("Connected to WebSocket server")
 

with open('pepper_text.json', 'r') as file:
    data = json.load(file)
    print("Contents of the JSON file:", data)

# Check if the file contains the word "switch on"
if "switch on" in data:
    # Send "lit_led" to the WebSocket server
    ws.send("lit_led")
    print("Sent: lit_led")

elif "switch off" in data:
    # Send "lit_led" to the WebSocket server
    ws.send("turnoff_led")
    print("Sent: turnoff_led")

else:
    print("No 'switch on' found in the file.")

# Gracefully close WebSocket connection
ws.close()
