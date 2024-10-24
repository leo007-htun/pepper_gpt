#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use executeJS Method"""

import qi
import argparse
import sys
import time

def main(session):
    """
    This example uses the executeJS method.
    To Test ALTabletService, you need to run the script ON the robot.
    """
    # Get the service ALTabletService.
    tabletService = session.service("ALTabletService")

        # Display a local web page located in boot-config/html folder
        # The ip of the robot from the tablet is 198.18.0.1


    with open('/home/cmpuser1/pepper_gpt/link.txt', 'r') as file:
        video_link = file.read()
        video_link = "'" + video_link + "'"

    tabletService.showWebview('https://www.youtube.com/watch?v=Qks5ICb7gGc')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="10.50.20.53",
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