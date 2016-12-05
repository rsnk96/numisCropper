import numpy as np
import cv2
import sys
import glob
import os
import natsort

cwd = os.getcwd()

os.chdir(sys.argv[1])

files = natsort.natsorted(glob.glob('*.*'))

if(not os.path.isdir('corrected')):
    os.mkdir('corrected')

for file in files:
    OG = cv2.imread(file,0)
    a = cv2.resize(OG, None, fx=0.25, fy=0.25)
    a = cv2.GaussianBlur(a, (31,31), 0)
    a = cv2.medianBlur(a, 9)

    thresh = cv2.adaptiveThreshold(a, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 9, 2)
    # ret, thresh = cv2.threshold(a, 100, 255, 1)

    kernel = np.ones((11,11), dtype=np.uint8)
    thresh2 = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=4)
    thresh = thresh2
    # thresh = cv2.medianBlur(thresh, 9)

    cont_img = thresh.copy()
    _,contours,hierarchy = cv2.findContours(cont_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  #contours[1:] because border of image also detected as a contour
    max_contour = contours[np.argmax(len(i) for i in contours)]
    max_contour = contours[-1]

    try:
        ellipse = cv2.fitEllipse(max_contour)
    except:
        print(file,': unable to fit ellipse')

    thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    cv2.ellipse(thresh, ellipse, (0,255,0), 2)

    
    '''coords = np.argwhere(thresh)
    x_coords, y_coords = np.sort(coords[:,0]), np.sort(coords[:,1])
    no_of_points = x_coords.shape[0]
    # print(x_coords)
    #NOTE: This will not be the same as the geometric mean, as coordinate axes are considered independent
    # print(y_coords)
    x_mean = np.mean(x_coords[int(no_of_points*0.05): int(no_of_points*0.95)])
    y_mean = np.mean(y_coords[int(no_of_points*0.05): int(no_of_points*0.95)])

    x_span = abs(2*(2*x_mean - x_coords[int(no_of_points*0.05)]-x_coords[int(no_of_points*0.95)]))
    y_span = abs(2*(2*y_mean - y_coords[int(no_of_points*0.05)]-y_coords[int(no_of_points*0.95)]))

    x_range = [max(0, int(x_mean-x_span/2)), min(int(x_mean+x_span/2), OG.shape[1])]
    y_range = [max(0, int(y_mean-y_span/2)), min(int(y_mean+y_span/2), OG.shape[0])]
    output_image = a[y_range[0]:y_range[1],x_range[0]:x_range[1]]
    cv2.circle(thresh, (int(y_mean), int(x_mean)), max(int(x_span), int(y_span)),128 )'''
    
    row_range = [max(0,4*ellipse[0][1]-4*ellipse[1][1]), min(4*ellipse[0][1]+4*ellipse[1][1],OG.shape[0]) ]
    column_range = [max(4*ellipse[0][0]-4*ellipse[1][0],0), min(4*ellipse[0][0]+4*ellipse[1][0],OG.shape[1])]
    output_image = OG[row_range[0]:row_range[1], column_range[0]:column_range[1]] 
    


    # cv2.namedWindow('output',0)
    # # cv2.imshow('output', np.hstack((thresh,thresh2)))
    # cv2.imshow('output', output_image)
    # if(cv2.waitKey()==ord('q')):
    #     break


    cv2.imwrite(os.path.join('corrected',file), output_image)


os.chdir(cwd)