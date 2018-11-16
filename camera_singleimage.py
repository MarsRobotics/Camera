## takes a single image and converts it to a cv2 image (ready for image processing)

from picamera import PiCamera, array
from time import sleep
import socket, pickle
import numpy as np
import cv2
import copy


with PiCamera() as camera:
  
  with array.PiRGBArray(camera) as output:
    camera.resolution = (320, 240)
    camera.framerate = 24	
    sleep(.25)
    current_img = np.empty((240*320*3), dtype=np.uint8)
    camera.capture(current_img, 'bgr')
    current_img = current_img.reshape((240, 320, 3))
    cv2.imwrite('image_simple.jpg',current_img)
    
    # CONSTANTS -- right now a blueish image #
    #TODO: determine good bounds for our nav. object (& figure out nav. object)
    RED_LOW = 0
    RED_HIGH = 25
    GREEN_LOW = 25
    GREEN_HIGH = 100
    BLUE_LOW = 0
    BLUE_HIGH = 255

    target_pixel_count = 0
    total_count = 240*320

    modified_img = copy.deepcopy(current_img)

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
            #print(dim2)
            target_pixel_count+=1
            modified_img[dim_i][dim_j] = [0, 255 ,0]
      dim_j = -1
    print(target_pixel_count)  
    
    cv2.imwrite('modified_image.jpg', modified_img)
    kernel = np.ones((3,3), np.uint8)
    
    #TODO: find optimal erode/dilate pattern 
    
    #erode for 2 iterations
    erosion = cv2.erode(modified_img, kernel, iterations = 2)
    cv2.imwrite('eroded_img.jpg', erosion)
    
    #dilate once
    dilation = cv2.dilate(erosion, kernel, iterations = 1)
    cv2.imwrite('dilation_following_erosion.jpg', dilation)
    
    # TODO (?)identify center of image
    # TODO: (?) try identifying left and right bounds 


    #TODO: continuously retrieve, process and display image 