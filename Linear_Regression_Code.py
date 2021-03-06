# -*- coding: utf-8 -*-
"""
Created on Thu May 24 14:33:54 2018

@author: ONAT

"""
#THIS IS FOR LINEAR REGRESSION

from scipy.stats import linregress
from scipy import stats
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
import graphviz # This will be useful when visualizing the graph ouf our decision tree.
from sklearn.tree import DecisionTreeClassifier
import pandas as  pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model
import xlrd
from sklearn import tree
import numpy as np
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

years = []
years_1 = []

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

for c in range(0, 582):
    cell = first_sheet.cell(c,4)
    years_1.append(cell.value)
    
for b in years_1: # We are picking year from full dates and including them to our "years" list.
    if "2000" in b:
        b = "2000"
        years.append(b) 
        
    elif "2001" in b:
        b = "2001"
        years.append(b)
        
    elif "2002" in b:
        b = "2002"
        years.append(b)
        
    elif "2003" in b:
        b = "2003"
        years.append(b)
        
    elif "2004" in b:
        b = "2004"
        years.append(b)
    
    elif "2005" in b:
        b = "2005"
        years.append(b)
        
    elif "2006" in b:
        b = "2006"
        years.append(b)
        
    elif "2007" in b:
        b = "2007"
        years.append(b)
    
    elif "2008" in b:
        b = "2008"
        years.append(b)
        
    elif "2009" in b:
        b = "2009"
        years.append(b)


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

X = combined
# Multidimensional array, 1st dimension: types of planes, 2nd dimension: reasons of crash
 
Y = survival_2
# 1D array: contains survival rates in integer form.  

years_num = []

for a in years: #Since the values in "years" are in the string format, we are typecasting them to int and adding to "years_num"
    years_num.append(int(a))

x_train = tp[0:555]
# Contains plane types and reasons of the crashes from 2000 to 2008

x_test = tp[555:]
# Contains plane types and reasons of the crashes in the year 2009.

y_train = survival_2[0:555]
# Contains survival rates belonging to the crashes from 2000 to 2008

y_test = survival_2[555:]
# Contains survival rates of the crashes in the year 2009.

years_train = years[0:555]

years_test = years[555:]
 
def estimate_coef(x, y): # Returns the coefficients of the linear regression line. (Returns m and b from "y = mx + b")
    # number of observations/points
    n = np.size(x)
 
    # mean of x and y vector
    m_x, m_y = np.mean(x), np.mean(y)
 
    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y*x - n*m_y*m_x)
    SS_xx = np.sum(x*x - n*m_x*m_x)
 
    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x
 
    return(b_0, b_1)
 
def plot_regression_line(x, y, b): #Plots the regression line
    # plotting the actual points as scatter plot
    plt.scatter(x, y, color = "m",
               marker = "o", s = 30)
 
    # predicted response vector
    y_pred = b[0] + b[1]*x
 
    # plotting the regression line
    plt.plot(x, y_pred, color = "g")
 
    # putting labels
    plt.xlabel('Years')
    plt.ylabel('Survival Rate (%)')
 
    # function to show plot
    plt.show()
 
def main():
    # observations
    x = np.array(years_num)
    y = np.array(survival_2)
 
    # estimating coefficients
    b = estimate_coef(x, y)
    print("Estimated coefficients:\nb_0 = {}  \
          \nb_1 = {}".format(b[0], b[1]))
 
    # plotting regression line
    plot_regression_line(x, y, b)
 
if __name__ == "__main__":
    main()
