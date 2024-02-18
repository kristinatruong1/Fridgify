import cv2
import cvlib as cv
import pymongo
from cvlib.object_detection import draw_bbox
from gtts import gTTS
from playsound import playsound
from pymongo import MongoClient
import api
from flask import Flask, render_template, Response, url_for, redirect, request
from cvlib.object_detection import draw_bbox
import recipes
import html
import pyttsx3

vid = Flask(__name__)
labels = []
global recipeNames 
global recipeIngr 
global recipeInstr 
global instr_list 
global cur_instr
stop = 0

# speech
def speech(words):
    engine = pyttsx3.init()
    engine.say(words)
    engine.runAndWait()


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
    global recipeNames, recipeIngr, recipeInstr
    filtered = recipes.filterFood(labels)
    ingredients =  "Your ingredients are " + " ".join(filtered)
    if (ingredients != "Your ingredients are "):
        speech(ingredients)
    recipeDict = recipes.getRecipes(filtered)
    recipeNames = recipeDict[0]
    recipeIngr = recipeDict[1]
    recipeInstr = recipeDict[2]
    return redirect(url_for('results')) 

@vid.route('/results')
def results():
    #send recipe names to HTML to display
    return render_template('results.html', recipe1=recipeNames[0], recipe2=recipeNames[1], recipe3=recipeNames[2], recipe4=recipeNames[3], recipe5=recipeNames[4])

@vid.route('/openR')
def openR():
    global cur_instr
    recipe_name = request.args.get('recipe')
    cur_instr = 0
    return redirect(url_for('fullrecipe', recipe_name=recipe_name)) 

@vid.route('/fullrecipe/<recipe_name>')
def fullrecipe(recipe_name):
    global recipeNames, recipeInstr, recipeIngr, cur_instr, instr_list
    instr = ""
    ingr = ""
    if (recipe_name == recipeNames[0]):
        instr = recipeInstr[0]
        ingr = recipeIngr[0]
    elif (recipe_name == recipeNames[1]):
        instr = recipeInstr[1]
        ingr = recipeIngr[1]
    elif (recipe_name == recipeNames[2]):
        instr = recipeInstr[2]
        ingr = recipeIngr[2]
    elif (recipe_name == recipeNames[3]):
        instr = recipeInstr[3]
        ingr = recipeIngr[3]
    else:
        instr = recipeInstr[4]
        ingr = recipeIngr[4]

    instr = instr.replace('[','')
    instr =instr.replace(']','')
    instr = instr.replace('"','')
    instr = instr.replace(',','\n\n')
    ingr = ingr.replace('[','')
    ingr = ingr.replace(']','')
    ingr = ingr.replace('"','')
    ingr = ingr.replace(',','\n\n')

    # set instr list
    instr_list = instr.split('\n') 

    return render_template('ingredients.html',name=recipe_name, instr=instr, ingr=ingr)

@vid.route('/recipe_back')
def recipe_back():
    return redirect(url_for('results')) 

@vid.route("/next_instr")
def next_instr():
    global instr_list, cur_instr
    recipe_name = request.args.get('recipe')
    if cur_instr < len(instr_list):
        text = instr_list[cur_instr]
        speech(text)
        cur_instr += 1
    return redirect(url_for('fullrecipe', recipe_name=recipe_name)) 