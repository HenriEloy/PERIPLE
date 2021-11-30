from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import re #email checking
import pandas as pd

################################ DATABASES to DATAFRAMES ################################

coeffInternet = 0.8 #Importance of the internet grades
coeffMachLearn = 0.01 #Importance of the machine Learning grades
coeffNbVoters = 0.2 #Importance of the nbr of voters
coeffDone = 0.4 #Importance of the grades from the experience (already done activities)
coeffChoice = 1 #importance of the choices


WayToUsers = "../DataBases/users.csv"
WayToActivities = "../DataBases/activities.csv"
WayToQuestions = "../DataBases/questions.csv"
WayToFinal = "../DataBases/CLASSEMENT FINAL ESSAI.csv"
WayToImages = "../images/"
WayToOpinions = '../DataBases/opinions.csv'

dfUsers = pd.read_csv(WayToUsers, sep=';', encoding='latin1').fillna(0) #Creation of the dataframe from the users dataset
dfActivities = pd.read_csv(WayToActivities, encoding='utf16').fillna(0) #Creation of the dataframe from the activities dataset
dfQuestions = pd.read_csv(WayToQuestions, sep=';', encoding='latin1') #Creation of the dataframe from the questions dataset
dfOpinions= pd.read_csv(WayToOpinions, encoding='latin1').fillna(0)

dfQuestions = dfQuestions.assign(answer=0,gradeDone=0) #Add of the answer column
dfActivities = dfActivities.assign(gradeDone=0,gradeChoice=0,totalGrade=0,alreadyDone=0) #Add the personal grade column (grade of the choices)

dfActivities['gradeDone'] = pd.to_numeric(dfActivities['gradeDone'], downcast='float') #Set the FinalGrade column to float
dfActivities['gradeChoice'] = pd.to_numeric(dfActivities['gradeChoice'], downcast='float') #Set the FinalGrade column to float
dfActivities['totalGrade'] = pd.to_numeric(dfActivities['totalGrade'], downcast='float') #Set the FinalGrade column to float

################################ Useful functions ####################################

def checkmail(email): 
    if(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)):
        return True
    else:
       return False
   
def Transform_perso_dataset(userid): 
    
    dfUsers = pd.read_csv(WayToUsers, sep=';', encoding='latin1').fillna(0) #Creation of the dataframe to access the new users

    
    maxi = 0
    mini = 0
    inTypes = False
    for column in dfUsers.columns :
        if column == "visit" : #Do not process if it is the user information
            inTypes = True
            
        if inTypes == True :
            value = float(dfUsers[column][userid])
            
            if value > maxi :
                maxi = value
                
            if value < mini :
                mini = value
    
    rangeMinMax = maxi - mini #Range of the grades
    
    if rangeMinMax != 0 :
        for quesID in dfQuestions.index :
            gradeRelative = dfUsers[dfQuestions['question'][quesID]][userid] - mini #Relative grade considering the worst one
            grade5 = 5 * (gradeRelative/rangeMinMax) #previous grade out of 5
            dfQuestions['gradeDone'][quesID] = round(grade5,4) #Writing of the final grade in the database
            
    global listDone
    listDone = dfUsers['ActivityDone'][userid].split(',')
    for i in range(len(dfActivities)-len(listDone)):
        listDone.append("0")
    
    dfUsers['ActivityDone'][userid] = ','.join(listDone)
    dfUsers.to_csv(WayToUsers, index=False, sep=';', encoding='latin1')
    
    for a in dfActivities.index :
        dfActivities['alreadyDone'][a] = listDone[a]
    
   
################################ INTERFACE ###########################################


#Define our different screens
class WelcomeWindow(Screen):
    pass

class LoginWindow(Screen):
        
    def try_login(self):
        
        dfUs = pd.read_csv(WayToUsers, sep=';', encoding='latin1').fillna(0) #Creation of the dataframe from the users dataset               
        pseudo = self.user.text
        password = self.password.text
        
        if(pseudo in dfUs['pseudo'].tolist()): #if this name exists in the pseudo column
            global userID
            userID = dfUs[dfUs['pseudo']==pseudo].index.tolist()[0] #save the first (and only) id with this pseudo
            
            if(dfUs['password'][userID] == password) : #if the password is the good one
                Transform_perso_dataset(userID)
                return True
            
            else :
                self.message.text = "Error on Pseudo or Password"
                return False
                userID = -1
                
        else :
            self.message.text = "Error on Pseudo or Password"
            return False     
    pass

class RegisterWindow(Screen):
    def try_register(self):
        
        dfUsers = pd.read_csv(WayToUsers, sep=';', encoding='latin1') #Creation of the dataframe from the users dataset
        
        email = self.email.text
        pseudo = self.pseudo.text
        password = self.password.text
        password2 = self.password2.text
        
        if checkmail(email) == True : #if the email is validate
            if pseudo not in dfUsers['pseudo'].tolist() : #if the pseudo does not exist yet
                if password == password2 :
                    new_row = {'id':len(dfUsers), 'email':email, 'pseudo': pseudo, 'password': password, 'ActivityDone': '0,0,0'}
                    dfUsers = dfUsers.append(new_row, ignore_index=True)
                    dfUsers.to_csv(WayToUsers, index=False, sep=';', encoding='latin1') #change the value on the csv
                    return True
                else:
                    self.message.text = "Passwords not concording"
                    return False
            else:
                self.message.text = "Pseudo already taken"
                return False
        else:
            self.message.text = "Enter valid email please"
            return False
                
    pass
        
class StartWindow(Screen):
    pass

class ChoiceWindow(Screen):
    
    def click0(self):
        return self.get_answers(0)
    
    def click1(self):
        return self.get_answers(1)
    
    def click2(self):
        return self.get_answers(2)
    
    def click3(self):
        return self.get_answers(3)
    
    def click4(self):
        return self.get_answers(4)
    
    def click5(self):
        return self.get_answers(5)
        
    def get_answers(self, answer):
        idQuestion = dfQuestions[dfQuestions['question']==self.questionName.text].index.tolist()[0]
        dfQuestions['answer'][idQuestion] = answer #store the answer
        if idQuestion < len(dfQuestions) :
            Qok = False
            n=1
            while Qok == False :
                if idQuestion+n < len(dfQuestions) :
                    if dfQuestions['link'][idQuestion+n] != 'NAN' :
                        idNext = dfQuestions[dfQuestions['question'] == dfQuestions['link'][idQuestion+n]].index.tolist()[0]
    
                        if dfQuestions['answer'][idNext]>2 :
                            self.resulttype.text = dfQuestions['link'][idQuestion+n]
                            self.questionName.text = dfQuestions['question'][idQuestion+n] #Show next question
                            Qok = True
                            return False
                        n+=1
                            
                    else:
                        self.resulttype.text = ""
                        self.questionName.text = dfQuestions['question'][idQuestion+n] #Show next question
                        Qok = True
                        return False
                else:
                    Qok = True
                    ShowResultWindow.ComputeAll()
                    return True
                    
        else:
            ShowResultWindow.ComputeAll()
            return True

        
    pass

class ResultWindow(Screen):
    
    pass


class ShowResultWindow(Screen):
        
    def ComputeAll():
        
        ############### COMPUTING PERSONAL GRADES ####################
    
        for a in dfActivities.index : #for any question (and answer)
        
            if dfActivities['alreadyDone'][a] == 1 or dfActivities['alreadyDone'][a] == '1' :
                dfActivities['totalGrade'][a] = 0
            else :
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
                
                average = float(round(sumAns/cnt,4)) #compute the grade out of 5
                dfActivities['gradeChoice'][a] = average #save it
                
                ################# COMPUTING THE DONE GRADE #################
                
                cntDone = 0
                sumDone = 0
                
                for d in range(len(listType)) : #foreach type
                    if listType[d] in dfQuestions['question'].tolist(): #if the type exists in the question dataframe
                        indexType = dfQuestions[dfQuestions['question']==listType[d]].index.tolist()[0] #Get the index of the type
                        doneAnswer = dfQuestions['gradeDone'][indexType] #get the done grade (out of 5) of this type
                        sumDone += doneAnswer
                        cntDone += 1
                
                averageDone = float(round(sumDone/cntDone,4)) #compute the grade out of 5
                dfActivities['gradeDone'][a] = averageDone #save it
                
            
                ################# COMPUTING THE TOTAL GRADE #################
                
                #Compute the totalGrade with 3 grades
                totalGrade = (dfActivities['OriginalGrade'][a] * coeffInternet + dfActivities['MLGrade'][a] * coeffMachLearn + dfActivities['gradeNbVoters'][a] * coeffNbVoters + dfActivities['gradeDone'][a] * coeffDone + dfActivities['gradeChoice'][a] * coeffChoice)/(coeffInternet+coeffMachLearn+coeffNbVoters+coeffDone+coeffChoice)
                
                dfActivities['totalGrade'][a] = round(totalGrade,5)
        
        dfFinal = dfActivities.sort_values(by = 'totalGrade', ascending = False)
        dfFinal.to_csv(WayToFinal, index=False, encoding='utf16') #change the value on the csv
        

    def getType(self, index,newdf): 
        if (newdf['Type 3'][index] == 0 or newdf['Type 3'][index] == '0') and (newdf['Type 4'][index] == 0 or newdf['Type 4'][index] == '0'):
            types = newdf['Type 1'][index] + " - " + newdf['Type 2'][index]
            
        else:
            
            if newdf['Type 4'][index] == 0:
                types = newdf['Type 1'][index] + " - " + newdf['Type 2'][index] + " - " + newdf['Type 3'][index]
                
            else:
                types = newdf['Type 1'][index] + " - " + newdf['Type 2'][index] + " - " + newdf['Type 3'][index] + " - " + newdf['Type 4'][index]
        
        return types

   
    def on_enter(self): #execute when the screen appears
        newdf = pd.read_csv(WayToFinal, encoding='utf16').fillna(0) #Creation of the dataframe from the personal dataset
        self.resultype.text = self.getType(0,newdf)
        self.resultname.text = newdf['name'][0]
        self.resultimage.source = WayToImages + newdf['image'][0]  
    
   
    def nextInfo(self):
        newdf = pd.read_csv(WayToFinal, encoding='utf16').fillna(0) #Creation of the dataframe from the personal dataset
        idnow = newdf[newdf['name']==self.resultname.text].index.tolist()[0]
        if idnow < len(newdf)-1 :
            idnext = idnow + 1
            self.resultype.text = self.getType(idnext,newdf)
            self.resultname.text = newdf['name'][idnext]
            self.resultimage.source = WayToImages + newdf['image'][idnext]
        
    def previousInfo(self):
        newdf = pd.read_csv(WayToFinal, encoding='utf16').fillna(0) #Creation of the dataframe from the personal dataset
        idnow = newdf[newdf['name']==self.resultname.text].index.tolist()[0]
        if idnow > 0:
            idprevious = idnow - 1
            self.resultype.text = self.getType(idprevious,newdf)
            self.resultname.text = newdf['name'][idprevious]
            self.resultimage.source = WayToImages + newdf['image'][idprevious]
            
    def liked(self): #like button
        idActivity = dfActivities[dfActivities['name']==self.resultname.text].index.tolist()[0] #get the id of the activity
        
        #add the like in the opinion file
        global userID
        global listDone
        if listDone[idActivity] == '0':
            print('like add')
            newrow={'id user':userID,'id activity':idActivity,'opinion':1}#add the like in the opinion file
            dfOp = dfOpinions.append(newrow,ignore_index=True)
            dfOp.to_csv(WayToOpinions,index=False, encoding='latin1')
            
            #change in the personal line in users
            listType = [dfActivities['Type 1'][idActivity], dfActivities['Type 2'][idActivity], dfActivities['Type 3'][idActivity], dfActivities['Type 4'][idActivity]] #List of the four types
            
            for i in range(len(listType)):
                if listType[i] in dfQuestions['question'].tolist(): #if this name exists in the name column            
                    dfUsers[listType[i]][userID] += 1
            
            listDone[idActivity] = "1"
            dfUsers['ActivityDone'][userID] = ','.join(listDone)
            
            dfUsers.to_csv(WayToUsers,index=False, sep=';', encoding='latin1')
            

        
    def disliked(self):
        idActivity = dfActivities[dfActivities['name']==self.resultname.text].index.tolist()[0] #get the id of the activity
        
        #add the like in the opinion file
        global userID
        global listDone
        if listDone[idActivity] == '0':
            print('dislike add')
            newrow={'id user':userID,'id activity':idActivity,'opinion':-1}#add the like in the opinion file
            dfOp = dfOpinions.append(newrow,ignore_index=True)
            dfOp.to_csv(WayToOpinions,index=False, encoding='latin1')
            
            #change in the personal line in users
            listType = [dfActivities['Type 1'][idActivity], dfActivities['Type 2'][idActivity], dfActivities['Type 3'][idActivity], dfActivities['Type 4'][idActivity]] #List of the four types
            
            for i in range(len(listType)):
                if listType[i] in dfQuestions['question'].tolist(): #if this name exists in the name column            
                    dfUsers[listType[i]][userID] += -1
                    
                listDone[idActivity] = "1"
                dfUsers['ActivityDone'][userID] = ','.join(listDone)
                    
                dfUsers.to_csv(WayToUsers,index=False, sep=';', encoding='latin1')
    
        
class Recalculate(Screen):
    
    def recalculate(self):
        global userID
        Transform_perso_dataset(userID)
        ShowResultWindow.ComputeAll()

class WindowManager(ScreenManager):
    pass


class PeripleApp(MDApp):
    
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file('essai.kv')     

PeripleApp().run()