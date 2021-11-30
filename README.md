# PERIPLE :world_map:
AI project for Hanyang university students

###### Group Members :  
Aurélien POUXVIEL, ESILV - France, aurelien.pouxviel@edu.devinci.fr  
Tristan d'ANTIN, ESILV - France, tristandantin@gmail.com  
Samuel PARIENTE, ESILV - France, samuel.pariente@edu.devinci.fr  
Alexandre MORLAT, ESILV - France, alexandre.morlat@edu.devinci.fr  
Henri ELOY, ESILV - France, henri.eloy@edu.devinci.fr  

Proposal : 

OPTION A

PERIPLE is an idea of startup we want to create, this is the project :  
It is a full personalized program which use machine learning and the choices from the user to create a perfect trip.  
We take in count activities rates from internet, but mainly rates, budget, timing given by the user.  
With that we are creating a perfect ordoned list of activities for the user and then propose an actual guide to him.  
We want to use datebases from internet, but we will complete and compare it with the rates of all our users.  
So the database will be unique for every user, gathering the database from internet, the database changed by the choices of all users (machine learning) and then the database from the answers the user gave.  
When starting the app, the user has to give his budget and time limits. Then he has to make several ratings (ex: rate 1 out of 5 "Monuments" and 3 out of 5 for "Restauration").   
At the end we will adapt the database as I said before and propose a final guide based on all of that.  

We're sorry if it isn't clear, we'll be really happy to discuss it with you.  

## I- Introduction
  ###### 1. Motivation

PERIPLE is a start-up idea that came to us when we were brainstorming on a topic for the AI and applications project. While we were exchanging on current innovative projects, we imagined a service to create a user-tailored tourism program. 
At the beginning of this semester in South Korea, such a tool would have proven to be greatly useful in order to optimize our tour days and to assist us in planning. Of course, effective tools are already established in the tourism market but we are thinking bigger. Moreover, we are convinced that artificial intelligence can revolutionize, or at least improve, the functioning of existing services. 



  ###### 2. Purpose
The idea is the following: to develop an artificial intelligence solution to predict what a tourist who wants to furnish his stay will like, and this from the analysis of a database, upstream. The intelligent algorithm would feed on three factors to propose a suitable activity program:
- The general opinions already existing on the activities
- Its opinion on what it has liked or disliked
- The coherence of the proposed program (in terms of distance between each activity, price, etc.)
But we are thinking bigger, and we even plan to develop a real powerful application, based on this famous algorithm, which would include the best of the market (visuals, functionalities, ergonomics) and possibly other essential functionalities (ticketing, GPS navigation, etc.).
Concretely, here is how we imagine a classic use of our application:
1.	The user launches the application and logs in/registers with his login and password;
2.	A quick questionnaire is launched on the kind of activities he is interested in (rather museums, monuments, nightlife, gourmet restaurant, fast food, etc.) and that he rates from 1 to 5 stars;
3.	Once the user's profile has been defined, he or she is offered a list of activities that he or she might enjoy.
4.	Once the user has gone to an activity, the application proposes to the user to click on Like/Dislike, which will further enhance the algorithm and propose more and more suitable activities.
You will find through our blog the totality of our steps and the whole explicitation of various realizations from the obtaining and the modification of the database, the elaboration of the processing/prediction algorithm to the programming of a prototype interface. We wish you an excellent reading, up to our excitement for our project and we apologize in advance if some misunderstandings remain because of a sometimes imperfect mastery of the English language.
## II- Datasets
  
introduction: 
As we needed specific information which was not already on a dataframe, we had to build it. 
First of all we built a template dataframe looks like that:
![variables](https://user-images.githubusercontent.com/92365536/144016463-ea3dd477-3081-4b72-af79-43e8f4e10107.PNG)
Part 1: Google Rating

Our two most important variables are the name and de rating associated. We had two choices: google rating or trip advisor rating. As google API are more accessible we choose Google: 
![Periple DataFrame](https://user-images.githubusercontent.com/92365536/144016584-7b9392cb-911f-49fb-9897-2f9463247219.png)

How to take this information for a lot of establishments? 
As we saw in the introduction template we need some types to define the places:

catering gastronomic local
catering gastronomic global
catering casual local
catering casual global
catering fastfood
catering original
activity sport practice
activity sport watch
activity fun
activity relaxation
activity show cinema
activity show theater
nightlife club
nightlife bar
visit museum historical
visit museum modern 
visit monument exterior
visit monument interior
visit walk nature
visit walk urban
  
Part 2: Google Place API

Nearby fonction: a google api function which takes 20 locations near gps coordinate in a ray and related to Keywords. 
For each “types ligne” we will make a request. However, at the end 20 establishments for one line is not enough. so we split in 4 smaller rays: 
![Periple DataFrame (1)](https://user-images.githubusercontent.com/92365536/144017780-56118a2e-2c23-4c23-a95e-d21f081b1740.png)


Part 3: Code 
We took 80 establishments for 20 “type lines” and delete duplicates. thanks to this [code](https://github.com/HenriEloy/PERIPLE/blob/8fc87fc18f8c55d24b6eea87df7c2bb683b16426/DataBases/builtdata.py).

![datafin](https://user-images.githubusercontent.com/92365536/144018095-d6d496ad-da2b-48f1-9827-83b7569434d1.PNG)

At the end we have 763 establishments of 20 different types associated with an image.


## III- Methodology

  To achieve this personal list of activities, we will use the data collected with google API (as we explained earlier), but we also obviously need data from the user.
  I will start by describing what a lambda user will see when opening our IA app, and then explain how we computed everything to find the perfect activities for him.
  
  First, we ask the user to create an account because we want to save some data that he will give us and use it only for this person.
  Once he is connected, we present him several 'types' of activities, and ask him to give a grade out of 5 for each of those types. It's good to know that types are sorted and organized in a tree, starting with main types (such as 'Visit' or 'Catering') in which there are more focused types (such as 'museums', then 'historical', etc.). You can see those trees just here: 
  
  <img width="487" alt="visits" src="https://user-images.githubusercontent.com/75729292/144012671-d5b21fb1-90de-4b77-8bfc-e6d1b631a6e8.PNG">
  <img width="416" alt="Catering" src="https://user-images.githubusercontent.com/75729292/144012713-67942d0d-8974-4f18-83f3-2eb30173df48.PNG">
  <img width="419" alt="Activity" src="https://user-images.githubusercontent.com/75729292/144012737-21c5e2ac-2180-4c76-b1d7-53f6b548e7ca.PNG">
  <img width="339" alt="Nightlife" src="https://user-images.githubusercontent.com/75729292/144012790-51f8ad62-2c31-44ad-a226-785f6fd76b0b.PNG">

In order to simplify and save time for the user, we don't ask him to give a grade to a type if he gave a bad one to the 'parent' category.

When he has graded all the types, we will show him the first activity we think he will like, and propose several options for each activity: to like or dislike the activity (after he did it or if he already did it on a previous trip), to see the next one, to come back to the last one, and finally, to recalculate everything, considering the activities he just liked or disliked.

That's it for our first version! Of course, we plan to go further after this semester, but we really focused on the algorithms and databases, to have a strong base for the future of PERIPLE.

Now, we must explain how we compute all our data, without using any of the known IA and machine learning models.

First, we have the database created with google API, we have 763 activities in Paris, and a lot of information about them. But for now, we just use several information: the name, the google grade (out of 5), the number of voters (for that google grade) and the three types for each activity 
Case in point: for the Louvre Museum, we get from google a grade of 4.7/5, with 223394 voters and the three types: Visit – Museum – Historical
(We will also use the image of each activity for the display at the end, but it’s useless for our algorithms)
To store our data, we are computing an average grade, calculated with 5 grades (we can easily change the coefficients of each of those grades to get the mode accurate prediction possible).

###### 1-	“Google grade”

  Not a lot of things to say about this one, it’s just the grade given by hundreds of google users, we have it on the database built previously with google API. (Example: 4.7/5 for Louvre Museum)
This grade has a coefficient of 0.8

###### 2-	“Voters grade”

  In order to separate the activities, and to favorize the most known (a 4.7 with 20 000 votes is more important than a 4.8 with 3 votes)
For that, we used a logarithmic scale (between 0 and 10 voters, the grade is between 0 and 1, between 11 and 100 voters, the grade is between 1 and 2, between 101 and 1000 voters, the grade is between 2 and 3, etc.). Because very few activities have a lot of voters, and it was impossible to compute it normally (a few good and a lot of small grades).
For example, with 223394 voters, Louvre Museum obviously gets a 5/5
This grade has a coefficient of 0.2

###### 3-	“Machine learning grade”

  Do you remember when we propose to the user to like or dislike an activity he has done ? When he does that, his opinion is used two times, and the first is right here. 
We save in a database all the opinions from the users, and, we created a program considering all the binary decisions and computing a grade out of 5 for each activity. We compute using an easy method, every activity is noted in relation to the more and the less liked one. So, the one with the more likes gets a 5 and the one with the more dislikes gets a 0. And all other ones are between them.
If this application were used by a lot of people, this machine learning could help us have our own grades for each activity, grades given by our users and not by all the users from internet.
For now, we obviously don’t have enough users to give this grade a real impact on the final grade, so the coefficient is for now 0.01

###### 4-	“Choices grade”

  As you can see, the three grades we already gave for each activity do not consider the choices or activities our logged user choose. They are the same for every user (the 3rd one can be changed by every user, for every user).

This 4th grade, is based on the preferences the logged user gave us. He gave, for each type, a grade out of 5. We just have to make an average of each grade for each activity with those types!
For example: if the user gave 3 to “Visit”, 5 to “Museum” and 4 to “Historical”, the Louvre Museum will get a “choice grade” of 4/5

That way, the choices of the user are considered. And the coefficient is 1 (the best one because we really want the user to visit things he really wants).

If it’s the first time the program computes the perfect activities for a user, we stop here, and make an average of those 4 grades with associated coefficients. We can then easily sort by the final grade which is the best activity for our user!

###### 5-	The “Already Done grade”

  This last grade is very important. As we said, when the user like, or dislike an activity (which means he did it), a second thing appends: we will save the id of the activity, to be sure not to propose him this activity again, and we will improve (or lower) the 5th grade of all activities sharing one, two or three types with the activity already done!
Of course, the more types there are in common, the more the grade will be changed!

We do that so when the user wants to visit again Paris (or any other city we will add after), or when he asks us to recalculate, we can consider what he already liked or disliked. 
It means, the more the user uses the application, the more it will be adapted to what he likes.

This grade has a coefficient of 0.4

We now have 5 different grades, and it’s easy for us to know what the perfect activity for him will be!


## IV- Evaluation and Analysis
  ###### Graphs, Tables or statistics

## V- Related Work
  ###### Tools, library or doc for this project

## VI- Conclusion/Discussion

To sum up this project, we have managed to operate in a structured way. We relied on tools such as communication tools, file sharing and task planning.  
We divided the tasks between us but all our work was linked, whether it is the algorithmic part, creation/finding of datasets, hosting thoses data, create a little graphic interface or analyse the data. 

And as said before, we intend to go further. We really want to pursue this project with the idea of making a startup.    
That's why we also worked on the development and not only the algorithmic part. We would be happy to have your feedback and we will continue to work hard on this project.   When we will return to France, we intend to take the necessary steps to create the company and also to get information from startup incubators, especially in our school which proposes some.
