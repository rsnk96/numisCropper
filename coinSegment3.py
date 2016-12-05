import cv2
import numpy as np
import os
import glob
import sys
import natsort

cwd = os.getcwd()

os.chdir(sys.argv[1])

files = natsort.natsorted(glob.glob('*.*'))

if(not os.path.isdir('corrected')):
    os.mkdir('corrected')

cv2.namedWindow('output',0)

for file in files:
    img = cv2.imread(file)

    img_copy = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
    img_copy = cv2.resize(img_copy, None, fx=0.25, fy=0.25)
    # canny = cv2.Canny(img_copy, 50,150)
    _, canny = cv2.threshold(img_copy, 150, 255, 1)

    kernel = np.ones((2,2), np.uint8)
    opening =  cv2.dilate(canny,kernel,iterations = 1)
    opening = cv2.medianBlur(opening, 9)
    opening = cv2.medianBlur(opening, 9)
    
    cont_img = opening.copy()
    _,contours,hierarchy = cv2.findContours(cont_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  #contours[1:] because border of image also detected as a contour
    max_contour = contours[np.argmax(list(len(i) for i in contours))]
    cv2.drawContours(cont_img, contours, np.argmax(list(len(i) for i in contours)), 255,8)

    try:
        ellipse = cv2.fitEllipse(max_contour)
        # ellipse_temp = cv2.fitEllipse(max_contour)
        # if(not ellipse_temp[1][1]<100):
        #     ellipse=ellipse_temp
    except:
        print(file,': unable to fit ellipse')

    thresh = cv2.cvtColor(img_copy, cv2.COLOR_GRAY2BGR)
    cv2.ellipse(thresh, ellipse, (0,255,0), 2)

    row_range = [max(0,4*ellipse[0][1]-4*ellipse[1][1]), min(4*ellipse[0][1]+4*ellipse[1][1],img.shape[0]) ]
    column_range = [max(4*ellipse[0][0]-4*ellipse[1][0],0), min(4*ellipse[0][0]+4*ellipse[1][0],img.shape[1])]
    output_image = img[int(row_range[0]):int(row_range[1]), int(column_range[0]):int(column_range[1])]

    # cv2.imshow('output', output_image)
    # if(cv2.waitKey()==ord('q')):
    #     break

    cv2.imwrite(os.path.join('corrected',file), output_image)


os.chdir(cwd)
