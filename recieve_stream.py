                      

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

    #print(frame) #debug
    cv2.imshow('ProcessedImage', frame)
    cv2.waitKey(1)
    

