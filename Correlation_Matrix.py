import xlrd
from sklearn import tree
import numpy as np
from sklearn import preprocessing
import graphviz # This will be useful when visualizing the graph ouf our decision tree.
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeRegressor

book = xlrd.open_workbook("new_airplane_data_2000.xlsx")
# We open our excel file where the data is stored. Contains data
# Belonging to plane accidents starting from 2000 to 2009.

first_sheet = book.sheet_by_index(0)

flight_type = [] # Types of planes in the crashes (military, cargo or civil aviation)

fatal = [] # Number of fatalities in the plane crashes
aboard = [] # Number of aboarded people in the plane crashes

for a in range(0, 582): # We are inserting the types of planes.
    cell = first_sheet.cell(a,0)
    flight_type.append(cell.value)

for a in range(0, 582): # We are inserting numbers of people who were aboard after the accidents.
    cell = first_sheet.cell(a,1)
    aboard.append(cell.value)
    
for a in range(0, 582): # We are inserting numbers of fatalities after accidents.
    cell = first_sheet.cell(a,2)
    fatal.append(cell.value)
    
    
"""" 
In our original data types of planes are not given clear fashion. We want to associate 
all planes with 3 main categories, which are "military", "cargo" and "civil aviation".
We do the sorting by looking at specific keywords in the original data strings.
 
Each type will have a code:
   
Military --> "1.0"
Cargo --> "2.0"
Civil Aviation --> "3.0"
    
"""
    
flight_type_1 = []
flight_type_2 = [] 
flight_type_3 = [] 

for b in flight_type: # We are sorting out military planes.
    # If the word contains the word "Military", then it is a military plane.
    if "Military" in b:
        b = "1.0"
        flight_type_1.append(b)        
    else:
        flight_type_1.append(b)
    
for b in flight_type_1: # We are sorting out cargo planes.
    # If the word contains "Cargo", "Carriers" or "FedEx", then it is a cargo plane.
    if "Cargo" in b:
        b = "2.0"
        flight_type_2.append(b) 
        
    elif "Carriers" in b:
        b = "2.0"
        flight_type_2.append(b)
        
    elif "FedEx" in b:
        b = "2.0"
        flight_type_2.append(b)
        
    else:
        flight_type_2.append(b)   
        

for b in flight_type_2: # We are sorting out civil aviation planes.
    # Rest of the planes must be civial aviation planes because there are no types to left to label the rest.
    if "1.0" not in b:
        if "2.0" not in b:
            b = "3.0"
            flight_type_3.append(b)
        else:
            flight_type_3.append(b)
    else:
        flight_type_3.append(b)
        
        
reason = [] # We will keep the reasons of the plane crashes.
survival = [] # Percentage of people survived at the plane crashes.
death = [] # Percentage of people died at the plane crashes.
        
for c in range(0, 582):
    cell = first_sheet.cell(c,3)
    reason.append(cell.value)

for c in range(0,582):
    death.append( (fatal[c]) * 100 / (aboard[c]) )
    
for d in range(0,582):
    survival.append(100.0 - death[d])


""" Since Sklearn can't handle categorical value when we are trying to fit a model with categorical attributes, we are encoding
those attributes with numbers. """

lab_enc = preprocessing.LabelEncoder()
encoded = lab_enc.fit_transform(flight_type_3)
encoded_2 = lab_enc.fit_transform(reason)

tp = np.array(encoded)
fp = np.array(encoded_2)

survival_2 = []

for a in survival:
    survival_2.append(int(a)) # We do this because float values are also considered as "categorical" as well.
    # However, integers will not create a problem.
    
combined = np.vstack((tp, fp)).T
# Multidimensional array, 1st dimension: types of planes, 2nd dimension: reasons of crash

import numpy

from numpy import corrcoef, sum, log, arange
from numpy.random import rand
from pylab import pcolor, show, colorbar, xticks, yticks

R= (numpy.corrcoef(combined))
pcolor(R)
colorbar()
yticks(arange(0.5,10.5),range(0,10))
xticks(arange(0.5,10.5),range(0,10))
show()