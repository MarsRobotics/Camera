###########################################
# stream rpi camera module video to port 12345
#
# Created 11.4.18 by Emily Peterson
# Last Updated 11.4.18 XX.XX.XX 
# Contributers: Emily Peterson, 
###########################################

## to view the image:
##	1. run this script
##	2. from wherever you want to view the stream 
##	   (must be on same network): vlc tcp/h264://ip_of_pi_here:12345/


from picamera import PiCamera
from time import sleep
import socket


with PiCamera() as camera:
  camera.resolution = (640, 480)
  camera.framerate = 24	

  #create a connection on port 12345 to send the feed to
  server_socket = socket.socket()
  server_socket.bind(('0.0.0.0', 12345))
  server_socket.listen(0)

  connection = server_socket.accept()[0].makefile('wb')
	
  try:
    camera.start_recording(connection, format='h264')
    camera.wait_recording(60) #hold the stream open for 60 seconds
    camera.stop_recording()
  finally:
    connection.close()
    server_socket.close()

''' random extra things which we can use for testing, etc


camera = PiCamera()

camera.start_preview()
sleep(10)
camera.stop_preview()

camera.start_preview() 
camera.annotate_text = "Egg" #contributed by a Senior Sociology Major
camera.start_recording('/home/pi/vid_example.h264')
sleep(20)
camera.stop_recording()
camera.stop_preview()


'''
