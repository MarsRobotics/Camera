# Camera

### created Nov 2018

Code to handle image processing and navigation for UP  Robotics 2018-2019

## take_single_image.py

Takes a single image, does simple color recognition/image processing and saves images. 
This is where to start testing image modification.

## send_stream.py & recieve_stream.py

receive_stream.py (server) is run from any machine on the network. Start this script first from the server host (AKA your laptop)

send_stream.py (client) is run from the pi. Update the IP constant at the top of this file with the server ip (the laptop)

Currently just sends unprocessed images at slow rate. 

## fast_vid_stream.py
Sends a video stream from camera to port 12345. View through the following command (using vlc on linux machine at the moment):
  ``` vlc tcp/h264://ip_of_pi_here:12345/ ```
