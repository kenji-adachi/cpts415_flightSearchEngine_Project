import sys
import pickle
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import dbQuery
import trip_rec as TripRec
from trip_rec import Node

qtCreatorFile = "mainwindow.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class flightMainwindow(QMainWindow):
    def __init__(self):
        super(flightMainwindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cityChangeAllow = True
        self.countryChangeAllow = True

        #table
        self.loadAllAirports()
        self.loadAllAirlines()


        #dropdowns
        self.loadCountryDropDown()
        self.loadSourceDestAirports()

        #country
        self.ui.airportCountryDrop.currentTextChanged.connect(self.APCountrydropDownChanged)
        self.ui.airlineCountryDrop.currentTextChanged.connect(self.ALCountrydropDownChanged)
        #city
        self.ui.airportCityDrop.currentTextChanged.connect(self.APCitydropDownChanged)


        #buttons
        self.ui.clearFilterAirport.clicked.connect(self.APclearFilters)
        self.ui.clearFilterAirline.clicked.connect(self.ALclearFilters)
        self.ui.findRoute.clicked.connect(self.find_route)

        #checkboxes
        self.ui.airlineCodeShareCheckBox.stateChanged.connect(self.codeShareChecked)
        self.ui.airlineStopCheckBox.stateChanged.connect(self.stopsChecked)

        #spinboxes
        self.ui.airlineSpinBox.valueChanged.connect(self.airlineStopsChanged)


    #Loads countries into country drop down for airports and airlines
    def loadCountryDropDown(self):
        self.countryChangeAllow = False
        dropDownItems = dbQuery.country_names() #get country list

        #initialize airport countries
        for i in range(len(dropDownItems)):
            self.ui.airportCountryDrop.addItem(dropDownItems[i])
        self.ui.airportCountryDrop.setCurrentIndex(-1)
        self.ui.airportCountryDrop.clearEditText()

        #initialize airline countries
        for i in range(len(dropDownItems)):
            self.ui.airlineCountryDrop.addItem(dropDownItems[i])
        self.ui.airlineCountryDrop.setCurrentIndex(-1)
        self.ui.airlineCountryDrop.clearEditText()
        self.countryChangeAllow = True


    #Loads cities into dropdown
    def loadCityDropDown(self, chosenCountry):
        self.cityChangeAllow = False
        self.ui.airportCityDrop.clear()
        dropDownItems = dbQuery.city_names_with_country(chosenCountry)
        #initialize city dropdown
        for i in range(len(dropDownItems)):
            self.ui.airportCityDrop.addItem(dropDownItems[i])
        self.ui.airportCityDrop.setCurrentIndex(-1)
        self.ui.airportCityDrop.clearEditText()
        self.cityChangeAllow = True


    def loadDataIntoTable(self,uiTable,tableData,headerLabelName):
        columnAmount = 1
        rowAmount = len(tableData)
        uiTable.setColumnCount(columnAmount)
        uiTable.setRowCount(rowAmount)
        uiTable.setHorizontalHeaderLabels(headerLabelName)
        #input rows
        curRowCount = 0
        for row in tableData:
            uiTable.setItem(curRowCount,0,QTableWidgetItem(str(row)))
            curRowCount += 1
    

    def loadAllAirports(self):
        resultTable = self.ui.airportSearchTableResults
        theTable = dbQuery.airport_names() #call db to get list of airports
        headerLabels = ["Airport"]
        self.loadDataIntoTable(resultTable,theTable,headerLabels)

    def loadAllAirlines(self):
        resultTable = self.ui.airlineSearchTableResults
        theTable = dbQuery.airline_names() #call db to get list of airports
        headerLabels = ["Airline"]
        self.loadDataIntoTable(resultTable,theTable,headerLabels)


    #airport dropdown option was selected this will be called
    def APCountrydropDownChanged(self):
        if self.countryChangeAllow == False:
            return
        countrySelection = self.ui.airportCountryDrop.currentText() #get the current dropdown selection
        headerLabels = ['Airport']
        theTable = dbQuery.airport_country_search(countrySelection) #call db to get list of airports with given country
        resultTable = self.ui.airportSearchTableResults
        self.loadDataIntoTable(resultTable,theTable,headerLabels)
        
        self.loadCityDropDown(countrySelection)


    #airline dropdown option was selected this will be called
    def ALCountrydropDownChanged(self):
        countrySelection = self.ui.airlineCountryDrop.currentText() #get the current dropdown selection
        headerLabels = ['Airline']
        theTable = dbQuery.airline_country_search(countrySelection) #call db to get list of airlines with given country
        resultTable = self.ui.airlineSearchTableResults
        self.loadDataIntoTable(resultTable,theTable,headerLabels)


    #airline dropdown option was selected this will be called for city
    def APCitydropDownChanged(self):
        if self.cityChangeAllow == False:
            return
        citySelection = self.ui.airportCityDrop.currentText() #get the current dropdown selection
        headerLabels = ['Airport']
        theTable = dbQuery.airport_city_search(citySelection) #call db to get list of airports with given country
        resultTable = self.ui.airportSearchTableResults
        self.loadDataIntoTable(resultTable,theTable,headerLabels)


    def APclearFilters(self):
        self.cityChangeAllow = False
        self.countryChangeAllow = False

        self.ui.airportCountryDrop.setCurrentIndex(-1)
        self.ui.airportCityDrop.setCurrentIndex(-1)
        self.loadAllAirports()
        
        self.cityChangeAllow = True
        self.countryChangeAllow = True
    
    def ALclearFilters(self):
        self.ui.airlineCountryDrop.setCurrentIndex(-1)
        self.ui.airlineCodeShareCheckBox.setChecked(False)
        self.ui.airlineStopCheckBox.setChecked(False)
        self.loadAllAirlines()

    def codeShareChecked(self):
        #self.ui.airlineCountryDrop.setCurrentIndex(-1)
        if self.ui.airlineCodeShareCheckBox.isChecked() == True:
            print("CodeShare checked, show data with codeshare")
        else:
            print("CodeShare off, show original data")

    def stopsChecked(self):
        if self.ui.airlineStopCheckBox.isChecked() == True:
            print("Stops Checked, Current Value: ",self.ui.airlineSpinBox.value())
        else:
            print("Stops off")

    def airlineStopsChanged(self):
        if self.ui.airlineStopCheckBox.isChecked() == True:
            print("Stops changed to: ",self.ui.airlineSpinBox.value())

    def find_route(self):
        self.ui.tripsResultsTable.clear()
        row = 0
        column = 0
        stops = self.ui.stopSpinBox.value()

        with open("data/adjList.txt", "rb") as myFile:
            adjList = pickle.load(myFile)

        airportA = self.ui.tripsSourceAirportBar.currentText()
        airportB = self.ui.tripsDestinAirportBar.currentText()
        routeList = TripRec.connect_cities(adjList, airportA, airportB, stops=stops)
        self.ui.tripsResultsTable.setRowCount(100)
        self.ui.tripsResultsTable.setColumnCount(100)

        for route in routeList:
            for airport in route:
                self.ui.tripsResultsTable.setItem(row, column, QTableWidgetItem(airport))
                column += 1
            column = 0
            row += 1

    def loadSourceDestAirports(self):
        dropDownItems = dbQuery.airport_names() #get airport list

        #initialize source airports
        for i in range(len(dropDownItems)):
            self.ui.tripsSourceAirportBar.addItem(dropDownItems[i])
        self.ui.tripsSourceAirportBar.setCurrentIndex(-1)
        self.ui.tripsSourceAirportBar.clearEditText()

        #initialize destination airports
        for i in range(len(dropDownItems)):
            self.ui.tripsDestinAirportBar.addItem(dropDownItems[i])
        self.ui.tripsDestinAirportBar.setCurrentIndex(-1)
        self.ui.tripsDestinAirportBar.clearEditText()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = flightMainwindow()
    window.show()
    sys.exit(app.exec_())






    #Other functions and code for reference below


    # for resizing
    # header = self.table.horizontalHeader()       
    # header.setSectionResizeMode(0, QHeaderView.Stretch)
    # header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
    # header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
    
    # def updateText(self):
    #     print("pushed")
    #     self.ui.label1.setText(self.ui.insertedTextBox.text())
    #     self.ui.insertedTextBox.clear()



    

    # def addToTables(self):
    #     headerLabels = ['Greet','W', 'riz', 'poop', 'pee']
    #     theTable = [('Hello', 'World', 1, 2, 3), ('Goodbye', 'World', 4, 5, 6)]
    #     columnAmount = len(theTable[0])
    #     rowAmount = len(theTable)
    #     self.ui.airportSearchTableResults.setColumnCount(columnAmount)
    #     self.ui.airportSearchTableResults.setRowCount(rowAmount)
    #     self.ui.airportSearchTableResults.setHorizontalHeaderLabels(headerLabels)
    #     curRowCount = 0
    #     for row in theTable:
    #         for col in range(0,columnAmount):
    #             self.ui.airportSearchTableResults.setItem(curRowCount,col,QTableWidgetItem(str(row[col])))
    #         curRowCount += 1


    #self.ui.button1.clicked.connect(self.updateText)