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
  Periple is an idea of a startup we want to create. ...
  ###### 2. Purpose

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
We took 80 establishments for 20 “type lines” and delete duplicates. thanks to this code.

![datafin](https://user-images.githubusercontent.com/92365536/144018095-d6d496ad-da2b-48f1-9827-83b7569434d1.PNG)

At the end we have 763 establishments of 20 different types associated with an image.


## III- Methodology
  ###### 1. Explication of our algorithms
  ###### 2. Explication of features or code

## IV- Evaluation and Analysis
  ###### Graphs, Tables or statistics

## V- Related Work
  ###### Tools, library or doc for this project

## VI- Conclusion/Discussion

To sum up this project, we have managed to operate in a structured way. We relied on tools such as communication tools, file sharing and task planning.  
We divided the tasks between us but all our work was linked, whether it is the algorithmic part, creation/finding of datasets, hosting thoses data, create a little graphic interface or analyse the data. 

And as said before, we intend to go further. We really want to pursue this project with the idea of making a startup.    
That's why we also worked on the development and not only the algorithmic part. We would be happy to have your feedback and we will continue to work hard on this project.   When we will return to France, we intend to take the necessary steps to create the company and also to get information from startup incubators, especially in our school which proposes some.
