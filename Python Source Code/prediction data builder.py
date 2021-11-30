# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 23:41:01 2021

@author: samue
"""
import requests
import pandas as pd
dflist = []
tag1= ['restaurant','restaurant','restaurant','restaurant','restaurant','restaurant','activité','activité','activité','activité','activité','activité','nightlife','nightlife','visite','visite','visite','visite','visite','visite']
tag2 = ['gastronomique','gastronomique','francais','étrangé','fastfood','atypique','sport','sport','fun','relaxation','cinema','théatre','discotheque','bar','musée','musée','monument','monument','marche','marche']
tag3 = ['francais','étrangé','','','','','faire','regarder','','','','','','','historical','moderne','exterieur','interieur','nature','urban']


type1 = ['catering','catering','catering','catering','catering','catering','activity','activity','activity','activity','activity','activity','nightlife','nightlife','visit','visit','visit','visit','visit','visit']
type2 = ['gastronomic','gastronomic','casual','casual','fastfood','original','sport','sport','fun','relaxation','show','show','club','bar','museum','museum','monument','monument','walk','walk']
type3 = ['gastronomic local','gastronomic global','casual local','casual global','','','practice','watch','','','cinema','theater','','','historical','modern','exterior','interior','nature walk','urban walk']

typep1 = ['1','1','1','1','1','1','2','2','2','2','2','2','3','3','4','4','4','4','4','4']
typep2 = ['5','5','6','6','7','8','9','9','10','11','12','12','13','14','15','15','16','16','17','17']
typep3 = ['18','19','20','21','0','0','22','23','0','0','24','25','0','0','26','27','28','29','30','31']

for i in range(0,20):
    for j in range(1,5):
        
        if tag3[i] == '':
            data = pd.read_csv('C:/Users/samue/Desktop/ia/periple/data/google data/old/database csv/' + tag1[i]+' '+ tag2[i] +str(j)+'.csv',encoding='UTF-8')
        if tag3[i] != '':
            data = pd.read_csv('C:/Users/samue/Desktop/ia/periple/data/google data/old/database csv/' + tag1[i]+' '+ tag2[i]+' '+tag3[i] +str(j)+'.csv',encoding='UTF8')
        for w in range(0,data.shape[0]):
            if w%2 !=0:
                data = data.drop(w)
        
        df = pd.DataFrame()
        df['id'] = 0
       
        df['OriginalGrade'] = data['results__rating']
        
        df['Type 1'] = typep1[i]
        df['Type 2'] = typep2[i]
        df['Type 3'] = typep3[i]
        df['name'] = data['results__name']
        df['Location'] = data['results__formatted_address']
        dflist.append(df)

frames = pd.DataFrame()
for i in range(0,len(dflist)):
    frames = pd.concat([frames,dflist[i]])
frames= frames.drop_duplicates(subset=['name'])
frames= frames.drop_duplicates(subset=['Location'])

for i in range (0,frames.shape[0]):
    frames.iloc[i,0] = i

frames=frames.replace('\|','',regex=True)
frames=frames.replace('\!','',regex=True)
frames=frames.replace('\?','',regex=True)
frames=frames.replace('\&','',regex=True)
frames=frames.replace('\@','',regex=True)
frames=frames.replace('\/','',regex=True)



frames.to_csv('C:/Users/samue/Desktop/ia/periple/dataforpredict.csv',index=False,encoding ='UTF-16',sep=',')