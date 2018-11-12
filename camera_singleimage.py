## takes a single image and converts it to a cv2 image (ready for image processing)

from picamera import PiCamera, array
from time import sleep
import socket, pickle
import numpy as np
import cv2


with PiCamera() as camera:
  
  with array.PiRGBArray(camera) as output:
    camera.resolution = (320, 240)
    camera.framerate = 24	
    sleep(2)
    img = np.empty((240*320*3), dtype=np.uint8)
    camera.capture(img, 'bgr')
    img = img.reshape((240, 320, 3))
    cv2.imwrite('image_simple.jpg',img)
