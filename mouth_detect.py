import cv2 
import numpy as np
import matplotlib.pyplot as plt




mouth_cascade = cv2.CascadeClassifier('cascade_files/haarcascade_mcs_mouth.xml')

def detection(img):
    if mouth_cascade.empty():
        raise IOError('Unable to load the mouth cascade classifier xml file')
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mouth_rects = mouth_cascade.detectMultiScale(gray, 1.1, 2)
    area_temp = 0
    i=0
    for (x,y,w,h) in mouth_rects:
        # y = int(y - 0.15*h)
        # cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 3)
        crop_img = img[y : y + h, x : x + w] 
        pixel_num = img.shape[0]*img.shape[1]*img.shape[2]
        if pixel_num > area_temp:
            area_temp = pixel_num
            h_temp = round(1.2*h)
            w_temp = round(1.2*w)
            x_temp = x
            y_temp = y
        i += 1
        
    crop_img = img[y_temp : y_temp + h_temp, x_temp : x_temp + w_temp]
        
    return crop_img



