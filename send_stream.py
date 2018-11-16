import picamera
from time import sleep
import socket, pickle
import numpy as np
import cv2
import sys
import struct
import copy
#This is Client (sends data)

IP = ''  #this is the source (laptop) to display feed
PORT = 54321

if __name__ == "__main__":
  with picamera.PiCamera() as camera:
    
    #with array.PiRGBArray(camera) as output:
    with picamera.PiCameraCircularIO(camera, size = 1) as stream:
        
        #connect to server socket (laptop)
        client_socket = socket.socket()
        client_socket.connect((IP, PORT))
        connection = client_socket.makefile('wb')

        img_counter = 0

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        while True:
            sleep(.01)
            
            #set cameraonfiguration
            camera.resolution = (320, 240)
            camera.framerate = 70	
            
            #capture image
            current_img = np.empty((240*320*3), dtype=np.uint8)
            camera.capture(current_img, 'bgr')

            #format data for sending
            data = pickle.dumps(current_img, 0)
            size = len(data)
            print("{}:{}".format(img_counter, size))
            
            #send over socket
            client_socket.sendall(struct.pack(">L", size) + data)
            img_counter +=1
