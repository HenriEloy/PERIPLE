# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 15:59:34 2021

@author: samue
"""

import pandas as pd
import random
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

temp = pd.read_csv('C:/Users/samue/Desktop/ia/periple/dataforpredict.csv',encoding ='UTF-16')

df = pd.DataFrame()

df['rate'] = temp['OriginalGrade']
df['Type1'] = temp['Type 1']
df['Type2'] = temp['Type 2']
df['Type3'] = temp['Type 3']


df['like'] = 0
for i in range(0,100):
     a = random.randrange(0,2)
     b = random.randrange(0,763)
     df['like'][b] = a  
    


#dependent variable 
Y = pd.DataFrame()
Y['like']=df['like']

#independent variable
X= df.drop(labels=['like'],axis =1)


X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size =0.75,random_state=0)
model = RandomForestClassifier(n_estimators= 2,random_state=0)
model.fit(X_train, Y_train)
prediction_test = model.predict(X_test)

print(metrics.accuracy_score(Y_test, prediction_test))
df['prediction'] = 0
for i in range(0,df.shape[0]):
    if(df['like'][i]==0):
        df['prediction'][i]=model.predict([[df['rate'][i],df['Type1'][i],df['Type2'][i],df['Type3'][i]]])
    


        
dfend=pd.read_csv('C:/Users/samue/Desktop/ia/periple/Gdatabase.csv', encoding = 'UTF16')

dfend['like'] = df['like']
dfend['prediction'] = df['prediction'].replace(1,'Will Like')

dfend.to_csv('C:/Users/samue/Desktop/ia/periple/data/prediction/prediction.csv')


