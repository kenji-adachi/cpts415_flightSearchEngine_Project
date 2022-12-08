# trip = sequence of connected routes
# Constructs an adjacency matrix for efficient use in other functions
import pymongo
from pymongo import MongoClient
import pandas as pd

client = pymongo.MongoClient("mongodb+srv://Username:Password@cluster0.b8r61v1.mongodb.net/?retryWrites=true&w=majority")
db = client['Cluster0'] # connects to our database

class Node:
    name : str
    id : str
    visited : bool

def construct_graph():
    airportList = create_port_list()
    routeList = create_route_list()
    index = 0
    counter = 0
    adjMatrixDict = dict()
    adjMatrix = [list(map(lambda x: (x,0), airportList))] * len(airportList) # k x k matrix, k = nodes, (Airport, adj)
    print("Constructing adjacency matrix....")
    for row in adjMatrix:
        for airport, adj in row:
            print(counter)
            if is_route(routeList, airportList[index], airport): # compares between airportList and the adjMatrix airportList
                adj = 1
            counter += 1
        adjMatrixDict[airportList[index].name] = row # might change this later, seems redundant
        index += 1
    print("Adjacency matrix constructed")
    return adjMatrixDict

def create_route_list():
    col = db['Route']
    routeList = []

    queryRun = col.find({})
    
    for result in queryRun:
        srcAirportID = result["SRC_AIRPORT_ID"]
        destAirportID = result["DEST_AIRPORT_ID"]
        print(srcAirportID)
        routeList.append((srcAirportID, destAirportID))
    return routeList

# queries the database and puts each airport into a node
def create_port_list():
    col = db['Airport'] # our data is divided into "collections"
    airportList = []

    queryRun = col.find({}) # retrieve entire collection

    for result in queryRun: # mongoDB stores result into a list, so we loop it
        newNode = Node()
        newNode.name = result["NAME"]
        newNode.id = str(result["AIRPORT_ID"])
        newNode.visited = 0
        airportList.append(newNode)
    return airportList

def is_route(routeList, airportA, airportB):
    print("Searching for route between ", airportA.name, " and ", airportB.name)
    # simple query to check if theres a route between the airports
    #col = db['Route'] # our data is divided into "collections"
    #queryRun = col.find({'$and': [
                        #{'SRC_AIRPORT_ID': airportA.id},
                        #{'DEST_AIRPORT_ID': airportB.id}
                        #]}) # retrieve entire collection
    #for result in queryRun:
        #return 1
    #return 0


def connect_cities(adjMatrix, airportA, airportB, stops = 0):  # stops is an optional var
    routeList = dfs(adjMatrix, airportA, airportB, [])
    if routeList[-1] is not airportB.name:
        print("No available route")
        routeList.clear()
    else:
        print(routeList)
    
# Depth-first search
def dfs(adjMatrix, node, finalNode, routeList):
    node.visited = 1
    routeList.append(node.name)
    if node.name == finalNode.name:
        return routeList
    for airport, adj in adjMatrix[node.name]:
        if adj and not airport.visited:
            dfs(adjMatrix, airport, finalNode, routeList)
    return routeList



# Creates a list of all nodes that are connected to node
def find_route(node):
    pass


adjMatrix = construct_graph()

A = Node()
A.name = "Goroka Airport"
B = Node()
B.name = "Mount Hagen Kagamuga Airport"
print ("Time to find your route")
#connect_cities(adjMatrix, A, B)

