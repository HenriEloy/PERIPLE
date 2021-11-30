# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 15:59:34 2021

@author: samue
"""

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import random
temp = pd.read_csv('C:/Users/samue/Desktop/ia/periple/dataforpredict.csv',encoding ='UTF-16')

df = pd.DataFrame()
df['id'] = temp['id']
df['rate'] = temp['OriginalGrade']
df['Type1'] = temp['Type 1']
df['Type2'] = temp['Type 2']
df['Type3'] = temp['Type 3']


df['like'] = 0
for i in range(0,100):
     a = random.randrange(0,2)
     b = random.randrange(0,763)
     df['like'][b] = a  
    



#sizes = df['rate'].value_counts(sort=1)
#print(sizes)

#dependent variable 
Y = pd.DataFrame()

Y['like']=df['like']

#independent variable
X= df.drop(labels=['like'],axis =1)
from sklearn.model_selection import train_test_split

X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size =0.7,random_state=30)

from sklearn.ensemble import RandomForestClassifier


model = RandomForestClassifier(n_estimators= 10,random_state=20)
model.fit(X_train, Y_train)

prediction_test = model.predict(X_test)


pred = X_test
pred['pred']= prediction_test
pred['true'] = Y_test
pred.sort_values(by = 'pred')
pred.to_csv('C:/Users/samue/Desktop/ia/periple/datapredicted.csv',index=False,encoding ='UTF-16',sep=',')

from sklearn import metrics
print(metrics.accuracy_score(Y_test, prediction_test))



