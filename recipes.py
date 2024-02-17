import pymongo
from pymongo import MongoClient

#connectng db
client = MongoClient("mongodb+srv://kristinatruongkyt:H1p3uuoCy8p37d5F@cluster0.g81sekr.mongodb.net/fridgifyRecipeData")
db = client.get_database('fridgifyRecipeData')
records = db.Recipes

#placeholder list of ingredients
ingredients = ["1/2 c. vinegar"]

#we would loop/change the index
pattern = "." + ingredients[0] + "."
query = {'ingredients': {'$regex': pattern, '$options': 'i'}}

print(list(records.find(query)))
print("\n")