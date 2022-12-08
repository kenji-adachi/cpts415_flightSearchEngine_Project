# Constructs an adjacency list and utilizes DFS to find available routes
import pymongo
from pymongo import MongoClient
import pandas as pd
import time
import pickle

client = pymongo.MongoClient("mongodb+srv://Username:Password@cluster0.b8r61v1.mongodb.net/?retryWrites=true&w=majority")
db = client['Cluster0'] # connects to our database

class Node:
    name : str
    id : str
    visited : bool

def construct_adj_list():
    col = db['Route']
    queryRun = col.find({})
    airportList, airportDict = create_port_list()
    
    # Finds all routes and creates a dict with key = src, val = dest
    for result in queryRun:
         srcAirportID = result["SRC_AIRPORT_ID"]
         destAirportID = result["DEST_AIRPORT_ID"]
         srcAirport = findNode(airportList, srcAirportID)
         destAirport = findNode(airportList, destAirportID)
         if srcAirport is not None and destAirport is not None: # our data set tends to have a lot of useless NULLs, we need to get rid of those
             if srcAirport.name not in airportDict.keys():
                 airportDict[srcAirport.name] = []
             airportDict[srcAirport.name].append(destAirport)
    return airportDict

# given the ID, retrieve the node from the airportList
def findNode(airportList, airportID):
    for airport in airportList:
        if airport.id == str(airportID):
            return airport

# queries the database and puts each airport into a node
def create_port_list():
    col = db['Airport'] # our data is divided into "collections"
    airportList = []
    airportDict = dict()
    queryRun = col.find({}) # retrieve entire collection

    for result in queryRun: # mongoDB stores result into a list, so we loop it
         newNode = Node()
         newNode.name = result["NAME"]
         newNode.id = str(result["AIRPORT_ID"])
         newNode.visited = 0
         airportList.append(newNode)
         airportDict[newNode.name] = []
    return airportList, airportDict

# helper function for connect_cities, given the name of an airport we turn it into a node
# dfs only accepts nodes, not strings
def init_node(airport):
    node = Node()
    node.name = airport
    node.id = 0
    node.visited = 0
    return node

def connect_cities(adjList, airportA, airportB, stops = 0):  # stops is an optional var
    A = init_node(airportA)
    B = init_node(airportB)

    routeList = adj_list_dfs(adjList, A, A, B, [], []) # A = start, A = current, B = final

    size = len(routeList)
    if size > 0:
        print(size, " available route(s) found")
    else:
        print("No available route(s) found")
    
    if stops > 0:
        stopList = [x for x in routeList if len(x) <= stops]
        stopSize = len(stopList)
        print(stopSize, " available route(s) within ", stops, " stops")
        print(stopList)

# Rough implementation of dfs recursively
def adj_list_dfs(adjList, start, node, finalNode, route, routeList):
    node.visited = 1
    route.append(node.name)
    if node.name == finalNode.name:
        routeList.append(route[:])
        node.visited = 0
        return routeList
    for airport in adjList[node.name]:
        #if adj and not airport.visited:
        if not airport.visited and airport.name != start.name: # not the most efficient, but im tired
            adj_list_dfs(adjList, start, airport, finalNode, route, routeList)
            route.pop()
            #node.visited = 0 # currently this dfs does not provide routes of the type A->B->E, A->C->B->E (B is marked as visited)
            # this line of code will allow those routes, but since our database is MASSIVE, we will hit the recursive max depth
    return routeList

# Testing purposes
#adjList = {"A": [B, C], "B": [D], "C": [E], "D": [E, A], "E": [F], "F": []}
# A -> F
# Sochi International Airport, Kazan International Airport, Astrakhan Airport

# Adjacency matrix construction
# This takes roughly 100 seconds, but only needs to be done once
print("Constructing adj list....")
t0 = time.time()
adjList = construct_adj_list()
t1 = time.time()
with open("data/adjList.txt", "wb") as adjListFile:
    pickle.dump(adjList, adjListFile)
print("Finished in: ", t1 - t0)

# Loading adjacency matrix
with open("data/adjList.txt", "rb") as myFile:
   adjList = pickle.load(myFile)

# Desired airports
airportA = "Sochi International Airport"
airportB = "Astrakhan Airport"

# Find route between AirportA and airportB
print("Finding route....")
t0 = time.time()
connect_cities(adjList, airportA, airportB, stops=3) # optional parameter "stops=x"
t1 = time.time()
print("Finished in: ", t1 - t0)