import pandas as pd

WayToActivities = "../DataBases/activities.csv"
WayToOpinions = "../DataBases/opinions.csv"

#creation of Activities dataframe, encoded for french characters, with 0 when no values given
dfActivities = pd.read_csv(WayToActivities, encoding='utf16').fillna(0)
dfActivities['MLGrade'] = pd.to_numeric(dfActivities['MLGrade'], downcast='float') #Set the FinalGrade column to float
dfActivities['gradeNbVoters'] = pd.to_numeric(dfActivities['gradeNbVoters'], downcast='float') #Set the FinalGrade column to float

dfOpinions = pd.read_csv(WayToOpinions) #creation of opinions dataframe

coeff = 5 #importance of the grades

for i in dfOpinions.index : #Going through the new opinions
    idActi = dfOpinions['id activity'][i] #Getting the id of the activity rated
    opi = dfOpinions['opinion'][i] #Getting the opinion (-1 or 1)
    actiPosition = dfActivities[dfActivities['id']==idActi].index.tolist()[0]
    dfActivities['Iagrade'][actiPosition] += opi #Add the opinion to the IAgrade

print(dfOpinions.columns)
dfOpinions = dfOpinions.iloc[0:0]
dfOpinions.to_csv(WayToOpinions, index=False)


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
    dfActivities['MLGrade'][i] = round(IAgradeCoeff,2) #Writing of the grade in the database


################################### Computation grade number of voters #############################################

## Then, we compute the final grade, graduating out of 'coeff' the IA grade
for j in dfActivities.index :
    if dfActivities['numberofrates'][j] <= 10 :
        IAgradeCoeff = (dfActivities['numberofrates'][j]/10) #previous grade out of 'coeff'
        dfActivities['gradeNbVoters'][j] = round(IAgradeCoeff,2) #Writing of the grade in the database
    elif dfActivities['numberofrates'][j] <= 100 :
        IAgradeCoeff = 1 + (dfActivities['numberofrates'][j]/100) #previous grade out of 'coeff'
        dfActivities['gradeNbVoters'][j] = round(IAgradeCoeff,2) #Writing of the grade in the database
    elif dfActivities['numberofrates'][j] <= 1000 :
        IAgradeCoeff = 2 + (dfActivities['numberofrates'][j]/1000) #previous grade out of 'coeff'
        dfActivities['gradeNbVoters'][j] = round(IAgradeCoeff,2) #Writing of the grade in the database
    elif dfActivities['numberofrates'][j] <= 10000 :
        IAgradeCoeff = 3 + (dfActivities['numberofrates'][j]/10000) #previous grade out of 'coeff'
        dfActivities['gradeNbVoters'][j] = round(IAgradeCoeff,2) #Writing of the grade in the database
    elif dfActivities['numberofrates'][j] <= 100000 :
        IAgradeCoeff = 4 + (dfActivities['numberofrates'][j]/100000) #previous grade out of 'coeff'
        dfActivities['gradeNbVoters'][j] = round(IAgradeCoeff,2) #Writing of the grade in the database
    else :
        dfActivities['gradeNbVoters'][j] = 5 #Writing of the grade in the database


dfActivities.to_csv(WayToActivities, sep=',', index=False, encoding='utf16')