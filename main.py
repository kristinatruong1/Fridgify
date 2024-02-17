import ScanImage
import recipes
from playsound import playsound

# take photo/get photo
items = ScanImage.scan()

# filter items and find recipes
filtered = recipes.filterFood(items)
ingredients =  "Your ingredients are " + " ".join(filtered)
ScanImage.speech(ingredients)
recipeList = recipes.getRecipes(filtered)
print(recipes)

# output text 
# prompt additional ingredients

# if button is clicked, generate recipes using the database

#
