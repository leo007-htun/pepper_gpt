import time
from naoqi import ALProxy

class FaceTrackAndNavi:
    def __init__(self, robot_ip_file_path):
        self.robot_ip = self.get_robot_ip_from_file(robot_ip_file_path)
        self.PORT = 9559
        self.tracker_service = ALProxy("ALTracker", self.robot_ip, self.PORT)
        self.targetName = "Face"
        self.faceWidth = 0.1

    def facetrack(self):
        # Add target to track
        self.tracker_service.registerTarget(self.targetName, self.faceWidth)

        # Check if target is lost
        target = self.tracker_service.isTargetLost()
        if target==False:
            print("Target lost, stopping FaceTrackAndNavi class")
            self.tracker_service.stopTracker()
            return False

        # Do other face tracking logic here
        print("Tracking face")
        return True

    def navi(self):
        navigationProxy = ALProxy("ALNavigation", self.robot_ip, self.PORT)
        navigationProxy.navigateTo(0.5, 0.2, [["SpeedFactor", 0.3]])


    def get_robot_ip_from_file(self, file_path):
        with open(file_path, 'r') as file:
            ip_addresses = file.readline().strip()
        return ip_addresses

    def moveforward(self):
        motion_service = ALProxy("ALMotion", self.robot_ip, self.PORT)
        x = 0.2
        y = 0.0
        theta = 0.0
        motion_service.moveTo(x, y, theta)
        print("Moving forward")

    def get_robot_ip_from_file(self, file_path):
        with open(file_path, 'r') as file:
            ip_addresses = file.readline().strip()
        return ip_addresses

if __name__ == "__main__":
    # Create instances of the classes
    facetrack_navi = FaceTrackAndNavi('robot_ip.txt')
    move_forward = MoveForward('robot_ip.txt')

    while True:
        try:
            # Check if the target is lost
            target = facetrack_navi.tracker_service.isTargetLost()

            if target==False:
                print("Target found, starting MoveForward class")

                if facetrack_navi.facetrack():
                    continue

                move_forward.moveforward()

            elif target==True:
                print("Target lost, starting FaceTrackAndNavi class")

                if not facetrack_navi.facetrack():
                    continue

                if not facetrack_navi.navi():
                    continue
                    
            time.sleep(1)
        except Exception as e:
            print(f"Error in main: {e}")
            break


