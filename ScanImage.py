import cv2
import cvlib as cv
import pymongo
from cvlib.object_detection import draw_bbox
from gtts import gTTS
from playsound import playsound
from pymongo import MongoClient
import api
from flask import Flask, render_template, Response, url_for, redirect
from cvlib.object_detection import draw_bbox
import recipes

vid = Flask(__name__)
labels = []
recipeNames = []
recipeIngr = []
recipeInstr = []
stop = 0

# speech
def speech(words):
    language = "en"
    output = gTTS(text=words, lang=language, slow=False)
    output.save("./sounds/found_items.mp3")
    playsound("./sounds/found_items.mp3")

# access camera
def scan():
    video = cv2.VideoCapture(0)

    while True:
        success, frame = video.read()
        bbox, label, conf = cv.detect_common_objects(frame) # box and label objects in video
        output_image = draw_bbox(frame, bbox, label, conf) # draw box
        ret, buffer = cv2.imencode('.jpg', output_image) #window
        output_image = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + output_image + b'\r\n') 
        
        # items found
        for item in label: # adds to list if not already in it
            if item not in labels:
                labels.append(item)

        if stop: # next button pressed to break out loop/window
            video.release()
            cv2.destroyAllWindows()
            break

@vid.route('/')
def index():
    return render_template('homedesktop.html')

@vid.route('/camera')
def camera():
    return render_template('camera.html')

@vid.route('/video_feed')
def video_feed():
    return Response(scan(), mimetype='multipart/x-mixed-replace; boundary=frame')

@vid.route('/end_video', methods=['POST'])
def end_video():
    stop = 1
    return redirect(url_for('results')) 

@vid.route('/results')
def results():
    # filter items and find recipes
    filtered = recipes.filterFood(labels)
    ingredients =  "Your ingredients are " + " ".join(filtered)
    #if (ingredients != "Your ingredients are "):
        #speech(ingredients)
    recipeDict = recipes.getRecipes(filtered)
    recipeNames = recipeDict[0]
    recipeIngr = recipeDict[1]
    recipeInstr = recipeDict[2]
        
    #send recipe names to HTML to display
    return render_template('results.html', recipe1=recipeNames[0], recipe2=recipeNames[1], recipe3=recipeNames[2], recipe4=recipeNames[3], recipe5=recipeNames[4])

@vid.route('/openR')
def openR():
    return redirect(url_for('fullrecipe')) 

@vid.route('/fullrecipe')
def fullrecipe():
    return
