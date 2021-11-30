# -*- coding: utf-8 -*-


"""
Created on Tue Nov  9 18:33:39 2021
cicles centers: 
48.884492312452565, 2.3323356443875225
48.870125890905655, 2.3784513942451184
48.833638750509046, 2.3452181817971343
48.85059567850748, 2.290887480547902
@author: Samuel Pariente
"""
import requests
import json
import pandas as pd
#Google API
tag1= ['restaurant','restaurant','restaurant','restaurant','restaurant','restaurant','activité','activité','activité','activité','activité','activité','nightlife','nightlife','visite','visite','visite','visite','visite','visite']
tag2 = ['gastronomique','gastronomique','francais','étrangé','fastfood','atypique','sport','sport','fun','relaxation','cinema','théatre','discotheque','bar','musée','musée','monument','monument','marche','marche']
tag3 = ['francais','étrangé','','','','','faire','regarder','','','','','','','historical','moderne','exterieur','interieur','nature','urban']
nomfichier =[]
urllist =[]
coord = '48.85059567850748, 2.290887480547902'
for i in range(0,2):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='+tag1[i]+'+'+tag2[i]+'+'+tag3[i]+'&location='+coord+'&radius=2500&key=YourGooglekye'
    urllist.append(url)
    nomfichier.append(tag1[i]+' '+tag2[i]+' '+tag3[i])
for i in range(2,6):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='+tag1[i]+'+'+tag2[i]+'&location='+coord+'&radius=2500&key=YourGooglekye'
    urllist.append(url)
    nomfichier.append(tag1[i]+' '+tag2[i])
for i in range(6,8):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='+tag1[i]+'+'+tag2[i]+'+'+tag3[i]+'&location='+coord+'&radius=2500&key=YourGooglekye'
    urllist.append(url)
    nomfichier.append(tag1[i]+' '+tag2[i]+' '+tag3[i])
for i in range(8,14):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='+tag1[i]+'+'+tag2[i]+'+'+'&location='+coord+'&radius=2500&key=YourGooglekye'
    urllist.append(url)
    nomfichier.append(tag1[i]+' '+tag2[i])
for i in range(14,20):    
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='+tag1[i]+'+'+tag2[i]+'+'+tag3[i]+'&location='+coord+'&radius=2500&key=YourGooglekye'
    urllist.append(url)
    nomfichier.append(tag1[i]+' '+tag2[i]+' '+tag3[i])
# Making a get request

for i in range(0,len(urllist)):
    response = requests.get(urllist[i])
    response = response.json()
    with open('C:/Users/samue/Desktop/ia/periple/databasejson/'+nomfichier[i]+'4.json', 'w') as outfile:
        json.dump(response, outfile)
        
#data exploitation       
dflist = []
tag1= ['restaurant','restaurant','restaurant','restaurant','restaurant','restaurant','activité','activité','activité','activité','activité','activité','nightlife','nightlife','visite','visite','visite','visite','visite','visite']
tag2 = ['gastronomique','gastronomique','francais','étrangé','fastfood','atypique','sport','sport','fun','relaxation','cinema','théatre','discotheque','bar','musée','musée','monument','monument','marche','marche']
tag3 = ['francais','étrangé','','','','','faire','regarder','','','','','','','historical','moderne','exterieur','interieur','nature','urban']

type1 = ['catering','catering','catering','catering','catering','catering','activity','activity','activity','activity','activity','activity','nightlife','nightlife','visit','visit','visit','visit','visit','visit']
type2 = ['gastronomic','gastronomic','casual','casual','fastfood','original','sport','sport','fun','relaxation','show','show','club','bar','museum','museum','monument','monument','walk','walk']
type3 = ['gastronomic local','gastronomic global','casual local','casual global','','','practice','watch','','','cinema','theater','','','historical','modern','exterior','interior','nature walk','urban walk']

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
        df['name'] = data['results__name']
        df['OriginalGrade'] = data['results__rating']
        df['Iagrade'] = 0
        df['MLGrade'] = 0
        df['gradeNbVoters'] = 0
        if 'results__price_level' in data:
            df['Price€'] = data['results__price_level']
        else:
            df['Price€'] = 0
        df['Location'] = data['results__formatted_address']
        df['numberofrates'] = data['results__user_ratings_total']
        df['TimeH'] = 0
        df['Unmissable'] = 0
        df['PlaceID'] = data['results__place_id']
        df['Type 1'] = type1[i]
        df['Type 2'] = type2[i]
        df['Type 3'] = type3[i]
        df['Type 4'] = 0
        df['photoID'] = data['results__photos__photo_reference']
        
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

frames['image'] = 0
for i in range(0,frames.shape[0]):
    frames['image'] =frames['name'] + '.png' 
frames.to_csv('C:/Users/samue/Desktop/ia/periple/GDatabase.csv',index=False,encoding ='UTF-16',sep=',')

#take images
df = pd.read_csv('C:/Users/samue/Desktop/ia/periple/GDatabase.csv')

for i in range(0,df.shape[0]):
    response = requests.get('https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference='+str(df.iloc[i,15])+'&key=YourGooglekye')
    
    with open('C:/Users/samue/Desktop/ia/periple/picture/'+str(df.iloc[i,1])+'.png', 'wb') as outfile:
        f = open('C:/Users/samue/Desktop/ia/periple/picture/'+str(df.iloc[i,1])+'.png', 'wb')
                    
            # save the raw image data to the file in chunks.
    for chunk in response:
        if chunk:
            f.write(chunk)
    f.close()


