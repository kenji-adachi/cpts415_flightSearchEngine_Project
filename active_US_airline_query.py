import pymongo
from pymongo import MongoClient
import pandas as pd
import json
import certifi

ca = certifi.where()

client = pymongo.MongoClient("mongodb+srv://Keagen:EK4AyxAleZd4kGOv@cluster0.b8r61v1.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)

db = client['Cluster0']
airline_collection = db["Airline"] 
airport_collection = db["Airport"] 
country_collection = db["Country"] 
plane_collection = db["Plane"] 
route_collection = db["Route"] 

# Check that "ACTIVE" value is equal to "Y" for every airline
airlineQuery = airline_collection.distinct( "AIRLINE_ID", {"ACTIVE" :"Y", "COUNTRY" : "United States"}) 

# Print the AIRLINE_ID of satisfying airlines
for row in airlineQuery: 
    print (row) 

