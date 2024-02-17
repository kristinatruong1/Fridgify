import pymongo
from pymongo import MongoClient
from api import MONGO_URL

# connectng db
client = MongoClient(MONGO_URL)
db = client.get_database('fridgifyRecipeData')
records = db.Recipes

ingredients = ["1/2 c. vinegar"]

pattern = "." + ingredients[0] + "."
query = {'ingredients': {'$regex': pattern, '$options': 'i'}}

print(list(records.find(query)))
print("\n")
