# -*- coding: utf-8 -*-

###########################################################
# This module receives results from the speechrecognition module and prints to console
#
# Syntax:
#    python scriptname --pip <ip> --pport <port>
#
#    --pip <ip>: specify the ip of your robot (without specification it will use the NAO_IP defined below
#
# Author: Johannes Bramauer, Vienna University of Technology
# Created: May 30, 2018
# License: MIT
###########################################################

# NAO_PORT = 65445 # Virtual Machine
NAO_PORT = 9559 # Robot


# NAO_IP = "127.0.0.1" # Virtual Machine
NAO_IP = "10.50.20.179" # Pepper default
PORT = 5567

from optparse import OptionParser
import naoqi
import time
import sys
from naoqi import ALProxy
import json
import os


class BaseSpeechReceiverModule(naoqi.ALModule):
    """
    Use this object to get call back from the ALMemory of the naoqi world.
    Your callback needs to be a method with two parameter (variable name, value).
    """

    def __init__( self, strModuleName, strNaoIp ):
        try:
            naoqi.ALModule.__init__(self, strModuleName )
            self.BIND_PYTHON( self.getName(),"callback" )
            self.strNaoIp = strNaoIp

            # Initialize ALAudioPlayer proxy
            self.au = ALProxy("ALAudioPlayer")

        except BaseException as err:
            print( "ERR: ReceiverModule: loading error: %s" % str(err) )

    # __init__ - end
    def __del__( self ):
        print( "INF: ReceiverModule.__del__: cleaning everything" )
        self.stop()

    def start( self ):
        memory = naoqi.ALProxy("ALMemory", self.strNaoIp, NAO_PORT)
        memory.subscribeToEvent("SpeechRecognition", self.getName(), "processRemote")
        print( "INF: ReceiverModule: started!" )


    def stop( self ):
        print( "INF: ReceiverModule: stopping..." )
        memory = naoqi.ALProxy("ALMemory", self.strNaoIp, NAO_PORT)
        memory.unsubscribe(self.getName())

        print( "INF: ReceiverModule: stopped!" )

    def version( self ):
        return "1.1"

    def processRemote(self, signalName, message):
        # Do something with the received speech recognition result
        self.au.playFile("/home/nao/blip.mp3", 1, 0)
        print(type(message), message)

        file_path = "/home/cmpuser1/pepper_gpt/pepper_text.json"  # Check the file path
        try:
            with open(file_path, "w") as file:
                json.dump(message, file)
            print("Message successfully written to file.")
        except Exception as e:
            print("An error occurred while writing to file:", e)
     
        
def get_robot_ip_from_file(file_path):
    # Open the text file in read mode
    with open(file_path, 'r') as file:
        # Read the IP address from the file and strip newline characters
        ip_addresses = file.readline().strip()
    return ip_addresses

def main():
    """ Main entry point

    """
    parser = OptionParser()
    parser.add_option("--pip",
        help="Parent broker port. The IP address or your robot",
        dest="pip")
    parser.add_option("--pport",
        help="Parent broker port. The port NAOqi is listening to",
        dest="pport",
        type="int")
    parser.set_defaults(
        #pip=NAO_IP,
        pport=NAO_PORT)

    (opts, args_) = parser.parse_args()
    #pip   = opts.pip
    ip_file_path = "ip.txt" 
    robot_ip = get_robot_ip_from_file(ip_file_path)
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = naoqi.ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       #pip,         # parent broker IP
       robot_ip,
       pport)       # parent broker port

    try:
        p = ALProxy("BaseSpeechReceiverModule")
        p.exit()  # kill previous instance
    except:
        pass
    # Reinstantiate module

    # Warning: ReceiverModule must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global BaseSpeechReceiverModule
    
    #BaseSpeechReceiverModule = BaseSpeechReceiverModule("BaseSpeechReceiverModule", pip)
    BaseSpeechReceiverModule = BaseSpeechReceiverModule("BaseSpeechReceiverModule", robot_ip)
    BaseSpeechReceiverModule.start()


    try:
    # auto-detection
        SpeechRecognition = ALProxy("SpeechRecognition")
        SpeechRecognition.start()
        SpeechRecognition.calibrate()
        SpeechRecognition.setAutoDetectionThreshold(3) #2
        SpeechRecognition.enableAutoDetection()  # Enable continuous speech detection
        #SpeechRecognition.start()
        while True:
            time.sleep(1)


    except KeyboardInterrupt:
        print
        print ("Interrupted by user, shutting down")
        myBroker.shutdown()
        sys.exit(0)

'''
    if(False):
        #one-shot recording for at least 5 seconds
        SpeechRecognition = ALProxy("SpeechRecognition")
        SpeechRecognition.start()
        SpeechRecognition.setHoldTime(5)
        SpeechRecognition.setIdleReleaseTime(1.7)
        SpeechRecognition.setMaxRecordingDuration(10)
        SpeechRecognition.startRecording()

    else:
        # auto-detection
        SpeechRecognition = ALProxy("SpeechRecognition")
        SpeechRecognition.start()
        #SpeechRecognition.setHoldTime(2.5)
        #SpeechRecognition.setIdleReleaseTime(1.0)
        #SpeechRecognition.setMaxRecordingDuration(10)
        #SpeechRecognition.setLookaheadDuration(0.5)
        #SpeechRecognition.setLanguage("de-de")
        SpeechRecognition.calibrate()
        SpeechRecognition.setAutoDetectionThreshold(5)
        SpeechRecognition.enableAutoDetection()
        SpeechRecognition.startRecording()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print
        print ("Interrupted by user, shutting down")
        myBroker.shutdown()
        sys.exit(0)'''


if __name__ == "__main__":
    main()
