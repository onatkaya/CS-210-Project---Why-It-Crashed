import xlrd
#from sklearn import tree
from sklearn.datasets import load_iris
import numpy as np
from sklearn import preprocessing 
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB




book = xlrd.open_workbook("new_airplane_data_2000.xlsx")
# we open our excel file where the data is stored
first_sheet = book.sheet_by_index(0)




flight_type = [] # list of plane types in the plane crashes

fatal = [] # list of fatalities in the plane crashes
aboard = [] # list of aboarded people in the plane crashes

for a in range(0, 582): # flight type
    cell = first_sheet.cell(a,0)
    flight_type.append(cell.value)

for a in range(0, 582): # aboard 
    cell = first_sheet.cell(a,1)
    aboard.append(cell.value)
    
for a in range(0, 582): # fatalities
    cell = first_sheet.cell(a,2)
    fatal.append(cell.value)

flight_type_1 = [] #military revision
flight_type_2 = [] #cargo revision
flight_type_3 = [] #civil aviation revision

reason = []
survival = []
death = []

for b in flight_type:
    if "Military" in b:
        b = "1.0"
        flight_type_1.append(b)        
    else:
        flight_type_1.append(b)
    
for b in flight_type_1:
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
        

for b in flight_type_2:
    if "1.0" not in b:
        if "2.0" not in b:
            b = "3.0"
            flight_type_3.append(b)
        else:
            flight_type_3.append(b)
    else:
        flight_type_3.append(b)
        
        
for c in range(0, 582): # reason
    cell = first_sheet.cell(c,3)
    reason.append(cell.value)

for c in range(0,582):
    death.append( (fatal[c]) * 100 / (aboard[c]) )
    
for d in range(0,582):
    survival.append(100.0 - death[d])


lab_enc = preprocessing.LabelEncoder()
encoded = lab_enc.fit_transform(flight_type_3)
encoded_2 = lab_enc.fit_transform(reason)

tp = np.array(encoded)
fp = np.array(encoded_2)

survival_2 = []

for a in survival:
    survival_2.append(int(a))
    
combined = np.vstack((tp, fp)).T

X = combined
Y = survival_2

x_train = X[0:555]
x_test = X[555:]


y_train = Y[0:555]
y_test = Y[555:]

clf = MultinomialNB()

# Train the model using the training sets 

clf.fit(x_train, y_train)
pred = clf.predict(x_test)

our_score = accuracy_score(pred, y_test)

print(our_score)
