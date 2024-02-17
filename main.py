import ScanImage
import recipes
from playsound import playsound

# take photo/get photo
items = ScanImage.scan()

# filter items and find recipes
filtered = recipes.filterFood(items)
ingredients =  "Your ingredients are " + " ".join(filtered)
if (ingredients != "Your ingredients are "):
    ScanImage.speech(ingredients)
recipeList = recipes.getRecipes(filtered)
print(recipeList)

# output text 
# prompt additional ingredients

# if button is clicked, generate recipes using the database

#
