                      

###########################################
# Get the video stream and process it with cv2
#
# Created 11.4.18 by Emily Peterson
# Last Updated 11.15.18 
###########################################
#
#import urllib.request
import cv2
import sys
import getopt
import socket
import pickle, pickletools, time
import numpy as np
import struct
import copy

#this is server aka recieves data on port

''' CONSTANTS '''
PORT = 54321
X = 64 #128#240
Y = 96 #160 #320

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
        total_count = X*Y


        current_img = img.reshape((X, Y, 3))
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

if __name__== "__main__":

  #create socket   
  server_socket = socket.socket()
  server_socket.bind(('', PORT))
  server_socket.listen(10)
  print('socket is created, bound and listening')

  #accept data stream from camera
  conn, addr = server_socket.accept()

  data = b""
  payload_size = struct.calcsize(">L")
  print("payload_size:{}".format(len(data)))

 # Iproc = ImageProc() #uncomment for processing server (laptop) side
   
  #continually process data and output to video feed 
  while True:
    while len(data) < payload_size:
        print("Done Recv: {}".format(len(data)))
        data += conn.recv(4096)
      
    print("Done Recv: {}".format(len(data)))

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))

    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data =data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data)
    #print(len(frame)) #debug

    frame = frame.reshape((X, Y, 3))

    #frame = Iproc.do_processing(frame) #uncomment for processing server (laptop) side
    #print(frame) #debug
    cv2.imshow('ProcessedImage', frame)
    cv2.waitKey(1)
    

