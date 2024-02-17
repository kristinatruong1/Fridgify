import pymongo
from pymongo import MongoClient
from api import MONGO_URL

client = MongoClient(MONGO_URL)

# food
food_dict = ["apple", "banana", "orange", "strawberry", "grape", "watermelon", "pineapple", "kiwi", "mango", "pear",
        "peach", "blueberry", "raspberry", "cherry", "lemon", "lime", "plum", "apricot", "avocado", "cranberry",
        "fig", "grapefruit", "pomegranate", "tangerine", "date", "kiwifruit", "melon", "papaya", "nectarine",
        "coconut", "passion fruit", "guava", "lychee", "dragonfruit", "persimmon", "blackberry", "boysenberry",
        "elderberry", "mulberry", "rhubarb", "quince", "kumquat", "starfruit", "durian", "jackfruit", "cantaloupe",
        "honeydew", "plantain", 
        "carrot", "lettuce", "tomato", "broccoli", "potato", "onion", "cucumber", "spinach", "pepper", "cabbage",
        "zucchini", "eggplant", "celery", "garlic", "mushroom", "green bean", "asparagus", "sweet potato",
        "cauliflower", "corn", "pea", "radish", "squash", "kale", "beet", "turnip", "brussels sprout", "artichoke",
        "parsnip", "fennel", "okra", "leek", "rhubarb", "bok choy", "collard greens", "endive", "arugula",
        "watercress", "swiss chard", "broccolini", "cabbage", "rutabaga", "jicama", "chard", "kohlrabi", "sorrel",
        "parsley", "scallion", "shallot",
        "beef", "chicken", "pork", "lamb", "fish", "shrimp", "salmon", "tuna", "bacon", "sausage", "ham", "turkey",
        "duck", "veal", "rabbit", "lobster", "crab", "clam", "mussel", "squid", "octopus", "scallop", "goose",
        "oyster", "trout", "snapper", "tilapia", "catfish", "swordfish", "cod", "anchovy", "haddock", "sardine",
        "bass", "perch", "halibut", "mahimahi", "crayfish", "crawfish", "pangasius", "quail", "venison", "elk",
        "bison", "buffalo", "carp", "sturgeon", "tripe", "liver", "kidney", "heart", "tongue", "brain", 
        "eggs", "milk", "flour", "salt", "oil", "butter", "sugar", "vinegar", "soy sauce", "ketchup", "honey", "mustard",
        "baking powder", "baking soda", "stock"
    ]

# connecting db
def filterFood(found):
     notfood = []
     for item in found:
          if not (item in food_dict):
            notfood.append(item)

     for item in notfood:
         found.remove(item)
     return found

def getRecipes(ingredients):
    db = client.get_database('fridgifyRecipeData')
    records = db.Recipes
    
    pattern = "." + ingredients + "."
    query = {'ingredients': {'$regex': pattern, '$options': 'i'}}
    recipes = list(records.find(query))

    return recipes
