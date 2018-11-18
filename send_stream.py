import picamera
from time import sleep
import socket, pickle
import numpy as np
import cv2
import sys
import struct
import copy
#This is Client (sends data)

IP = '10.0.0.77'  #this is the source (laptop) to display feed
PORT = 54321

class ImageProc():

  def do_processing(self, img, bl=0, bh=225, gl=25, gh=100, rl=0, rh=25):

   # Image selection bounds
    
    RED_LOW = rl
    RED_HIGH = rh 
    GREEN_LOW = gl
    GREEN_HIGH = gh
    BLUE_LOW = bl
    BLUE_HIGH = bh

    target_pixel_count = 0
    total_count = 240*320


    current_img = img.reshape((240, 320, 3))
    modified_img = current_img #copy.deepcopy(current_img)

    #note: format is ordered BGR
    dim_i = -1
    dim_j = -1
    
    #checks for pixels within specified range 
    for dim1 in current_img:
      dim_i+=1
      for dim2 in dim1:
          dim_j+=1
          if (dim2[0] >= BLUE_LOW and dim2[0] <= BLUE_HIGH \
          and dim2[1] >= GREEN_LOW and dim2[1] <= GREEN_HIGH \
          and dim2[2] >= RED_LOW and dim2[2] <= RED_HIGH):
            target_pixel_count+=1
            modified_img[dim_i][dim_j] = [0, 255 ,0]
      dim_j = -1 
    
    kernel = np.ones((3,3), np.uint8)
    
    #erode for 2 iterations
    erosion = cv2.erode(modified_img, kernel, iterations = 2)
    
    #dilate once
    dilation = cv2.dilate(erosion, kernel, iterations = 1)
    return dilation
    

if __name__ == "__main__":
  with picamera.PiCamera() as camera:
    
    #with array.PiRGBArray(camera) as output:
    with picamera.PiCameraCircularIO(camera, size = 1) as stream:
        
        ip = ImageProc()
        #connect to server socket (laptop)
        client_socket = socket.socket()
        client_socket.connect((IP, PORT))
        connection = client_socket.makefile('wb')

        img_counter = 0

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        while True:
            sleep(.1)
            
            #set cameraonfiguration
            camera.resolution = (320, 240)
            camera.framerate = 10
            
            #capture image
            current_img = np.empty((240*320*3), dtype=np.uint8)
            camera.capture(current_img, 'bgr')

            current_img = ip.do_processing(current_img)
            

            #format data for sending
            data = pickle.dumps(current_img, 0)
            size = len(data)
            print("{}:{}".format(img_counter, size))
            
            #send over socket
            client_socket.sendall(struct.pack(">L", size) + data)
            img_counter +=1
