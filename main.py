import ScanImage
import recipes
from playsound import playsound
import threading

# take photo/get photo
def run_flask_app():
    ScanImage.vid.run(debug=True)

def main():
    # Start the Flask app on a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()
    ScanImage.vid.run(debug=True)
    items = ScanImage.getLabels()

    # filter items and find recipes
    filtered = recipes.filterFood(items)
    ingredients =  "Your ingredients are " + " ".join(filtered)
    if (ingredients != "Your ingredients are "):
        ScanImage.speech(ingredients)
    recipeDict = recipes.getRecipes(filtered)
    recipeNames = recipeDict[0]
    recipeIngr = recipeDict[1]
    recipeInstr = recipeDict[2]
    
    #send recipe names to HTML to display
    print(recipeNames)

# when button click display the ingrident 

# if button is clicked, generate recipes using the database

#
if __name__ == "__main__":
    main()