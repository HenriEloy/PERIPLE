import pandas as pd

WayToActivities = "../Databases/activities.csv"
WayToOpinions = "../Databases/opinions.csv"

#creation of Activities dataframe, encoded for french characters, with 0 when no values given
dfActivities = pd.read_csv(WayToActivities, sep=';', encoding='latin1').fillna(0)
dfOpinions = pd.read_csv(WayToOpinions, sep=';') #creation of opinions dataframe

#dfActivities['FinalGrade'] = pd.to_numeric(dfActivities['FinalGrade'], downcast='float') #Set the FinalGrade column to float

coeff = 1 #percentage of importance of the IA grades

print(dfActivities)

for i in dfOpinions.index : #Going through the new opinions
    idActi = dfOpinions['id activity'][i] #Getting the id of the activity rated
    opi = dfOpinions['opinion'][i] #Getting the opinion (-1 or 1)
    dfActivities['Iagrade'][idActi] += opi #Add the opinion to the IAgrade

##################### Computation of the final grade ########################

## First, we find the max and min of IAgrade among activities
## so we could compute the IA grade out of something
maxi = 0
mini = 0

for i in dfActivities.index :
    
    if dfActivities['Iagrade'][i] > maxi :
        maxi = dfActivities['Iagrade'][i]
        
    if dfActivities['Iagrade'][i] < mini :
        mini = dfActivities['Iagrade'][i]

rangeMinMax = maxi - mini #Range of the IAgrades
    
## Then, we compute the final grade, graduating out of 'coeff' the IA grade
for i in dfActivities.index :
    IAgradeRelative = dfActivities['Iagrade'][i] - mini    #Relative IAgrade considering the worst one
    IAgradeCoeff = coeff * (IAgradeRelative/rangeMinMax) #previous grade out of 'coeff'
    Fgrade = dfActivities['OriginalGrade'][i] + IAgradeCoeff #Sum of the original grade (from internet) with the new IA one
    dfActivities['FinalGrade'][i] = round(Fgrade,2) #Writing of the final grade in the database

print(dfActivities)
#Replacing csv by the modified dataframe, using ';' as separator and encoding for french characters
dfActivities.to_csv(WayToActivities, index=False, sep=';', encoding='latin1')