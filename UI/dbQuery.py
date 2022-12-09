import pymongo
from pymongo import MongoClient
import pandas as pd
import json
import certifi

ca = certifi.where()

#client = pymongo.MongoClient("mongodb+srv://Kenji:KzgUfPvjx9vlkQXg@cluster0.b8r61v1.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
client = pymongo.MongoClient("mongodb+srv://Keagen:EK4AyxAleZd4kGOv@cluster0.b8r61v1.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)

db = client['Cluster0']
airline_collection = db["Airline"] 
airport_collection = db["Airport"] 
country_collection = db["Country"] 
plane_collection = db["Plane"] 
route_collection = db["Route"] 

# Given a country name, return list of all active airlines (airline ID's) in that country
def airline_country_search(country_name):
    airline_list = []

    # Check that "ACTIVE" value is equal to "Y" for every airline
    airlineQuery = airline_collection.distinct( "NAME", { "ACTIVE" : "Y", "COUNTRY" : country_name } ) 

    # Print the AIRLINE_ID of satisfying airlines
    for row in airlineQuery: 
        airline_list.append(row)

    return(airline_list)

# Given a country name, return list of all airports (airport ID's) in that country
def airport_country_search(country_name):
    airport_list = []

    airportQuery = airport_collection.distinct( "NAME", { "COUNTRY" : country_name } )

    for row in airportQuery: 
        airport_list.append(row)

    return(airport_list)

# Given a city name, return list of all airports (airport ID's) in that city
def airport_city_search(city_name):
    airport_list = []
 
    airportQuery = airport_collection.distinct( "NAME", { "CITY" : city_name } )

    for row in airportQuery: 
        airport_list.append(row)

    return(airport_list)

# Return list of all valid airport names in database
def airport_names():
    airport_list = []

    airportQuery = airport_collection.distinct( "NAME", { "NAME" : { "$ne" : " " } } )

    for row in airportQuery:
        airport_list.append(row)
    airport_list = airport_list[1:]
    return(airport_list)

# Return list of all valid airline names in database
def airline_names():
    airline_list = []

    airlineQuery = airline_collection.distinct( "NAME", { "NAME" : { "$ne" : " " } } )

    for row in airlineQuery:
        airline_list.append(row)

    return(airline_list)

# Return list of all valid country names in database
def country_names():
    country_list = []

    countryQuery = country_collection.distinct( "COUNTRY", { "COUNTRY" : { "$ne" : " " } } )

    for row in countryQuery:
        country_list.append(row)

    return(country_list)

# Return list of all valid city names in database
def city_names():
    city_list = []

    cityQuery = airport_collection.distinct( "CITY", { "CITY" : { "$ne" : " " } } )

    for row in cityQuery:
        city_list.append(row)

    city_list = city_list[1:]
    return(city_list)

# Return list of all valid city names in database
def city_names_with_country(country_name):
    city_list = []

    cityQuery = airport_collection.distinct( "CITY", { "CITY" : { "$ne" : " " }, "COUNTRY" : country_name } )

    for row in cityQuery:
        city_list.append(row)
    city_list = city_list[1:]
    return(city_list)



#Print all query test lists
def main():
    country_name = "Madagascar"
    city_name = "Seattle"

    # print(airline_country_search(country_name))
    # print(airport_country_search(country_name))
    # print(airport_city_search(city_name))
    print(airport_names())
    # print(airline_names())
    # print(country_names())
    # print(city_names())

    


if __name__ == "__main__":
    main()