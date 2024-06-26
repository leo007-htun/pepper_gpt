#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use Dictionary TTS Methods (Japanese)"""

import qi
import argparse
import sys


def main(session):
    """
    This example uses the Dictionary TTS methods.
    It adds and removes words in the dictionary from the module.
    """
    # Get the service ALTextToSpeech.

    tts = session.service("ALTextToSpeech")
    try :
        tts.setLanguage("French")
    except RuntimeError:
        print "You need to install Japanese language in order to hear correctly these sentences."
    #Check the pronunciation before changing the dictionary
    tts.say("De rien! Si vous avez d'autres questions ou besoin d'aide supplémentaire, n'hésitez pas à demander. Je suis là pour vous aider!")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="10.50.20.110",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)