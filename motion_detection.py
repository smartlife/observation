import os
import re
import cv2
import numpy as np
import time
from matplotlib import pyplot as plt

class MotionDetector:
    def __init__(self):
        self.fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
        
    def observe(self, filename):
        img = cv2.imread(filename, cv2.IMREAD_COLOR)
        fgmask = self.fgbg.apply(img)
        changed = fgmask.sum().sum() / fgmask.shape[0] / fgmask.shape[1]
#         
        # cv2.imshow('image',img)
        # cv2.imshow('mask',fgmask)
        
        return changed
    
# img = cv2.imread('watch.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('лица/я.jpg', cv2.IMREAD_COLOR)
# cv2.imshow('image',img)
# edges = cv2.Canny(img, 50, 150)
# cv2.imshow('Edges', edges)
if __name__ == '__main__':
    path = "движение/фон1"
    
    motion = MotionDetector()
    
    for filename in sorted(os.listdir(path)):
        if not filename.endswith(".jpg"):
            continue
        filename = os.path.join(path, filename)
        changed = motion.observe(filename)
        print(changed)
        # break
        time.sleep(.900)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        # break
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()