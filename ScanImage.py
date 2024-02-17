import cv2
import cvlib as cv
import pymongo
from cvlib.object_detection import draw_bbox
from gtts import gTTS
from playsound import playsound
from pymongo import MongoClient
import api

# access camera
def scan():
    video = cv2.VideoCapture(0)
    labels = []

    while True:
        ret, frame = video.read()
        bbox, label, conf = cv.detect_common_objects(frame) # box and label objects in video
        output_image = draw_bbox(frame, bbox, label, conf) # draw box
        cv2.imshow("Object Detect", output_image) #window
        
        # items found
        for item in label: # adds to list if not already in it
            if item not in labels:
                labels.append(item)

        if cv2.waitKey(1) & 0xFF == ord("q"): #click q to break out loop/window
            video.release()
            break
    return labels
