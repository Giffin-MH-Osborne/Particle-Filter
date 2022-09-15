
from matplotlib import pyplot as plt
import numpy as np
from random import randint
import cv2

from copy import copy
from Line import Line
from constants import X_COORD, Y_COORD, MOE


MAX = None
MIN = None

PIXELS = []
LINES = []

#use openCV to read the image into a numpy array
def read_image(path) -> any:
    img = cv2.imread(path)
    return img

#convert the image to grayscale
def convert_to_grayscale(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return gray

#apply a guassian blur to the image
def gauss_blur(gray):
    kernel_size = 5
    blur = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    return blur

#apply the cannu algorithm to the blurred image
def canny(blur):
    low_thres = 40
    high_thres = 120
    edges = cv2.Canny(blur, low_thres, high_thres)
    return edges

#apply the hough algorithm to the image after canny edge detection
def hough(edges):
    rho = 1
    theta = np.pi/180
    threshold = 1
    min_line_length = 10
    max_line_gap = 1
    return cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

#find the largest and smallest Lines detected by the hough lines algorithm   
def find_bounds():
    global MAX, MIN

    MAX = max(LINES)
    MIN = min(LINES)

#process image into a numpy array and return the bounds  
def process_floor_plan(img_path):
    img = read_image(img_path)
    gray = convert_to_grayscale(img)
    blur = gauss_blur(gray)
    edges = canny(blur)
    lines = hough(edges)
    line_image = np.copy(img)

    for line in lines:
        for x1,y1,x2,y2 in line:
            new_line = Line((x1,y1),(x2,y2), (255, 0 ,0))            
            LINES.append(new_line)

    find_bounds()

    return MAX, MIN

#test the computer vision methods if this file is run as main       
if __name__ == "__main__":
    img_path = 'img/floor_plan_1.png'
    img = read_image(img_path)
    plt.imshow(img)
    plt.show()

    gray = convert_to_grayscale(img)
    blur = gauss_blur(gray)

    plt.imshow(blur)
    plt.show()

    edges = canny(blur)
    plt.imshow(edges)
    plt.show()

    lines = hough(edges)
    line_image = np.copy(img)

    for line in lines:
        for x1,y1,x2,y2 in line:
            new_line = Line((x1,y1),(x2,y2), (255, 0 ,0))            
            LINES.append(new_line)

    find_bounds()

    for line in LINES:
        line.display()
        cv2.line(line_image, line.start, line.end, line.colour, 5)

    combo = cv2.addWeighted(img, 0.8, line_image, 1, 0)

    plt.imshow(combo)
    plt.show()

    
        
        
        