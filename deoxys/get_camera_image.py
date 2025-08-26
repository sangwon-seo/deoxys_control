# Purpose: To get the image observation from realsense camera
# Author: Prem Raj
import rospy
from sensor_msgs.msg import Image
import cv_bridge
import cv2
import lockfile

class CameraRedisSubInterface:
    def __init__(self, camera_id=1):
        self.camera_id = camera_id
        self.filename = 'tmp/current_image_from_camera_{0}.png'.format(self.camera_id)

    def get_img_info(self):
        with lockfile.LockFile(self.filename):
            output_image = cv2.imread(self.filename)
        # print(image.dtype)
        # output_image = cv2.convertScaleAbs(image)
        return output_image


cam = CameraRedisSubInterface()
img = cam.get_img_info()
print(img.dtype)
print(img.shape)