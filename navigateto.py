# -*- encoding: UTF-8 -*-

import argparse
from naoqi import ALProxy


def get_robot_ip_from_file(file_path):
    # Open the text file in read mode
    with open(file_path, 'r') as file:
        # Read the IP address from the file and strip newline characters
        ip_addresses = file.readline().strip()
    return ip_addresses

def main(robotIP, PORT = 9559):

    navigationProxy = ALProxy("ALNavigation", robotIP, PORT)
    faceProxy = ALProxy("ALFaceDetection", robotIP, PORT)
    #motionProxy     = ALProxy("ALMotion", robotIP, PORT)
    postureProxy    = ALProxy("ALRobotPosture", robotIP, PORT)
    tablet    = ALProxy("ALTabletService", robotIP, PORT)

    # Wake up robot
    #motionProxy.wakeUp()

    # Send robot to Stand Init
    postureProxy.goToPosture("StandInit", 0.5)

    # No specific move config.
    while True:
        try:
            tablet.showImage('home/nao/gpt.png')
            navigationProxy.navigateTo(2.0, 0.0,[["SpeedFactor", 0.3]])
            faceProxy.subscribe("Test_Face",300, 0.0)
            navigationProxy.navigateTo(2.0, 0.0,[["SpeedFactor", 0.5]])
        except:
            pass
'''while True:
        try:
            if faceProxy.subscribe("Test_Face", 0.0):
                navigationProxy.moveAlong(["Composed", ["Holonomic", ["Line", [1.0, 0.0]], 0.0, 5.0]])
            else:
                navigationProxy.navigateTo(1.0, 0.0)
        except:
            pass
'''


    # To do 6 cm steps instead of 4 cm.
    #motionProxy.moveTo(1.0, 0.0, 0.0, [["MaxStepX", "0.06"]])

    # Will stop at 0.5m (FRAME_ROBOT) instead of 0.4m away from the obstacle.
    #navigationProxy.setSecurityDistance(0.5)


if __name__ == "__main__":
    ip_file_path = "ip.txt"
    robotIP = get_robot_ip_from_file(ip_file_path)
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default=robotIP,
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    
    main(args.ip, args.port)