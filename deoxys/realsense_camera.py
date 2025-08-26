# Purpose: To get the image observation from realsense camera
# Author: Prem Raj
import rospy
from sensor_msgs.msg import Image
import cv_bridge
import cv2
import lockfile

class Camera:
    def __init__(self, camera_id=1):
        self.camera_id = camera_id

        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.image_callback)

        self.image_start = False
        self.image_ready = False
        self.cur_image = None
        self.filename = 'tmp/current_image_from_camera_{0}.png'.format(self.camera_id)

    def image_callback(self,data):
        if self.image_start:
            try:
                self.image_start = False
                self.cur_image = cv_bridge.CvBridge().imgmsg_to_cv2(data, "bgr8")
                self.image_start = True
                rospy.sleep(0.1)
                with lockfile.LockFile(self.filename):
                    cv2.imwrite(self.filename,self.cur_image)
                # date_string = time.strftime("%Y-%m-%d-%H:%M")
                # print('image callback')
                self.image_ready = True
            except cv_bridge.CvBridgeError as e:
                print(e)

    def start(self):
        self.image_start = True
        print('Node is saving images at folder /tmp')

    def get_img_info(self):
        output_image = self.process_for_deoxys_standard()
        self.image_ready = False
        return output_image

    def process_for_deoxys_standard(self):
        while not self.image_ready:
            print('waiting for image to ready')
        return self.cur_image


rospy.init_node('camera')
cam = Camera(camera_id=1)
cam.start()
# rospy.Rate(10)
rospy.spin()
img = cam.get_img_info()
print(img.shape)