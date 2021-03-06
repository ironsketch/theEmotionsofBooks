# Emotional text - Machine Learning

#### Michelle Bergin

## Intro

First off, it is very hard for me to learn something if I do not dive deep and pull out it's guts. With that said, I wasn't really going to learn how to utilize machine learning tactics if I didn't build my own program from the bottom up.

My goal was to find the emotions of text!

I researched on the internet and found a data set that I downloaded called NRCcsvEmotion.csv which is from this website:
https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm

This data set has a HUGE dictionary of words in multiple languages. each word has a 10 int array attached to it. The ints are either 0 or 1. 1 represents that an emotion is related to it.

-- Example: --
English (en),Positive,Negative,Anger,Anticipation,Disgust,Fear,Joy,Sadness,Surprise,Trust
abandon,0,1,0,0,0,1,0,1,0,0

## Preparing the data:

To prepare the data I not only cleaned up the text instances but also the NRC data set. The NRC data set had many languages but I am only looking at English. So I cleaned out all other translations. Also, I am not interested in words that have no emotions tied to it. Some words had all 0's. For example : crate,0,0,0,0,0,0,0,0,0,0. So when I import the NRC data set I remove all 0'd elements.

To prepare text I just clean out symbols not needed and I use the generic python split() method that autmoagically splits for spaces. I lowercase everything and only use words that are in the NRC data set.

## Setting up the training set:

I have asked my community (online, school, friends, family) to submit paragraphs for me with one of the 10 emotions defined but not listed in the paragraph. An example of disgust:

How could someone put pineapple on their pizza? Merely the sight of it puts pits in my stomach. Imagining the taste makes me double over and gag.

Each txt is labeled with the emotion related and I parse that out to create my y set.

emotionDict = {"positive" : 0, "negative" : 1, "anger" : 2, "anticipation" : 3, "disgust" : 4, "fear" : 5, "joy" : 6, "sadness" :  7, "surprise" : 8, "trust" : 9}

So in total I have 10 classes.

## Creating the machine learning training and test set:

Once I have a list of all words related to each txt I shuffle and seperate a training and test set for y and x given a seperation percentage. Casually I just use 30% split.

## Machine Learning

### SGDClassifier

I first decided to start small and go for the one vs all approach to better learn how to do machine learning. So I did all anger or not, or all disgust or not. etc.

I imported the scikit learns Stochastic Gradient Descent. I set of the classifier and I train my data on whether it is or is not the emotion I am looking for and then fit my data. To test if it is classifying correctly I then use scikits predict method to see if it predicts correctly. Which, if I have more than 3 instances, it always predicts correctly. Any less and errors occur.

## Cross Validation

I set up a cross validation with my SGDClassifier but since my training set is SO small my accuracy is crazy low. Splitting my data for the training set at 40% I get:

[0.75, 0.875, 0.85714286] 

This is with 3 folds.

## BaseEstimator and Never 8 Classifier

I then used a base estimator for when it is never 8 my accuracy went up!

[0.875, 0.875, 0.85714286]

## Confusion Matrix

Running confusion matrix gives me:

[[16  2]

 [ 4  0 ]]

2 was wrongly classified as a text about surprise. 4 were wrongly cassified as not surprised.

## Precision and Recall

These are VERY low. More than likely because I have such a little test base!

0.2
0.3333333333333333

## F1 Score

.25 Which is from favoring precision and recall

## Threshold Curve

What am I looking at?

## Fuzzy Logic

What is printed represents each emotion and the degree of correctness for each emotion for each text. In the real world most experiences are an amalgamation of many emotions. 

## The Normal Equation

From the print out it appears that there is only one theta for each class...

[ 4.28598897  0.81045702  0.26536352 -0.50024168  0.27435619  0.11305699  

-0.13021756 -1.23335824 -0.37148055  0.53958076 -0.28161495]

But now it seems we can use this for predictions
Except I don't understand my book at this part so skipping.

## PyPlot

So I tried plotting my x_train and y_train and I noticed it is either 0 or 1 so that means that I need to possibly use a logistic regression model!

## Logistic Regression Model

I should be able to use this but I am not sure how or what to plot... So I am thinking about my fuzzy logic needs. 

## Decision Tree

I created a multiclass decision tree and then I loaded the book, Alice in Wonderland. I then ran it through the decision tree to find the probability of the book in each class. Unfortunately I got returned 1 or 0's ...

## How to use:

You need to tell the program what folder or file you want it to look at. And for training (so far how I have built this) you need to label your files with and underscore and the name of the emotion. For ex, meow_joy.txt

Your files need to be txt.

Example runs:

python3 bookEmotion.py meow_joy.txt

python3 bookEmotion.py /train
