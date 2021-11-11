import pandas as pd

coeffGeneral = 1 #Importance of the general grades
coeffDone = 1 #Importance of the grades from the experience (already done activities)
coeffChoice = 1 #importance of the choices


WayToUsers = "../DataBases/users.csv"
WayToActivities = "../DataBases/activities.csv"
WayToQuestions = "../DataBases/questions.csv"

dfUsers = pd.read_csv(WayToUsers, sep=';', encoding='latin1') #Creation of the dataframe from the users dataset
dfActivities = pd.read_csv(WayToActivities, sep=';', encoding='latin1') #Creation of the dataframe from the activities dataset
dfQuestions = pd.read_csv(WayToQuestions, sep=';', encoding='latin1') #Creation of the dataframe from the questions dataset
dfQuestions = dfQuestions.assign(answer=0) #Add of the answer column
dfActivities = dfActivities.assign(gradeDone=0,gradeChoice=0,totalGrade=0) #Add the personal grade column (grade of the choices)

dfActivities['gradeDone'] = pd.to_numeric(dfActivities['gradeDone'], downcast='float') #Set the FinalGrade column to float
dfActivities['gradeChoice'] = pd.to_numeric(dfActivities['gradeChoice'], downcast='float') #Set the FinalGrade column to float
dfActivities['totalGrade'] = pd.to_numeric(dfActivities['totalGrade'], downcast='float') #Set the FinalGrade column to float

##### Connection #####

userID = -1 #creating the variable
connected = False #Connected boolean

while connected == False: #while the connection is not a success
    
    pseudo = str(input("pseudo : ")) #Ask for the pseudo
    password = str(input("password : ")) #Ask for the password
    
    if(pseudo in dfUsers['pseudo'].tolist()): #if this name exists in the pseudo column
        userID = dfUsers[dfUsers['pseudo']==pseudo].index.tolist()[0] #save the first (and only) id with this pseudo
        
        if(dfUsers['password'][userID] == password) : #if the password is the good one
            print('succesfully connected')
            connected = True
        else :
            print('incorrect password !')
            userID = -1
            
    else :
        print('No user with this pseudo')
    
##### Get the personal dataset ######

listPerso = dfUsers['ListGeneral'][userID].split(',')
listPerso = list(map(int, listPerso)) # change the type of the list to int

## Let improve the list length (to match the number of activities)

missingValues = len(dfActivities) - len(listPerso) #For that, we compute the number of missing values

for i in range(missingValues) :
    listPerso.append(0) #We had 0 for each missing grade

############### Transform those grades in grades out of 5
maxi = 0
mini = 0

for i in range(len(listPerso)) :
    
    if listPerso[i] > maxi :
        maxi = listPerso[i]
        
    if listPerso[i] < mini :
        mini = listPerso[i]

rangeMinMax = maxi - mini + 1 #Range of the grades

for i in dfActivities.index :
    gradeRelative = listPerso[i] - mini #Relative grade considering the worst one
    grade5 = 5 * (gradeRelative/rangeMinMax) #previous grade out of 5
    dfActivities['gradeDone'][i] = round(grade5,2) #Writing of the final grade in the database
    
    
## Let write back this bigger list in the csv
listPerso = list(map(str, listPerso)) # change the type of the list to str
listSTR = ','.join(listPerso) #transform the list to string
dfUsers['ListGeneral'][userID] = listSTR #put it back in the dfUsers dataframe

dfUsers.to_csv(WayToUsers, index=False, sep=';', encoding='latin1') #change the value on the csv


############### ASKING PREFERENCES ####################

for q in dfQuestions.index : #for every question

    if dfQuestions['link'][q] == "NAN" : #If it's one of the basis questions
       
        answer = int(input(dfQuestions['question'][q])) #Ask for a value about the considered question
        dfQuestions['answer'][q] = answer #store the answer
        
    else :
        idLink = dfQuestions[dfQuestions['question']==dfQuestions['link'][q]].index.tolist()[0] #get the id of the linked question
    
        if dfQuestions['answer'][idLink]>2: #If the answer to the linked question is enough
            
            answer = int(input(dfQuestions['question'][q])) #Ask for a value about the considered question
            dfQuestions['answer'][q] = answer #store the answer

############### COMPUTING PERSONAL GRADES ####################

for a in dfActivities.index : #for any question (and answer)

    ############### COMPUTING PERSONAL CHOICES GRADES ####################

    listType = [dfActivities['Type 1'][a], dfActivities['Type 2'][a], dfActivities['Type 3'][a], dfActivities['Type 4'][a]] #List of the four types

    cnt = 0
    sumAns = 0
    
    for t in range(len(listType)) : #foreach type
        if listType[t] in dfQuestions['question'].tolist(): #if the type exists in the question dataframe
            indexQuestion = dfQuestions[dfQuestions['question']==listType[t]].index.tolist()[0] #Get the index of the question/answer of this type
            answer = dfQuestions['answer'][indexQuestion]
            sumAns += answer
            cnt += 1
    
    average = float(round(sumAns/cnt,2)) #compute the grade out of 5
    dfActivities['gradeChoice'][a] = average #save it
    
    ################# COMPUTING THE TOTAL GRADE #################
    
    #Compute the totalGrade with 3 grades
    totalGrade = dfActivities['FinalGrade'][a] * coeffGeneral + dfActivities['gradeDone'][a] * coeffDone + dfActivities['gradeChoice'][a] * coeffChoice
    dfActivities['totalGrade'][a] = round(totalGrade,2)
       
dfActivities = dfActivities.sort_values(by = 'totalGrade', ascending = False)

dfActivities.to_csv("../DataBases/CLASSEMENT FINAL ESSAI.csv", index=False, sep=';', encoding='latin1') #change the value on the csv
   