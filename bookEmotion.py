import os
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn import linear_model
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.base import BaseEstimator
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, precision_recall_curve
from sklearn.tree import DecisionTreeClassifier

tenEmotions = ["Positive", "Negative", "Anger", "Anticipation", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust"]

class Never8Classifier(BaseEstimator):
    def fit(self, x, y=None):
        pass
    def predict(self, x):
        return np.zeros((len(x), 1), dtype=bool)

def load_emotion_data(name):
    cleanEmotions = []
    emotionData = list(csv.reader(open(name, "r"), delimiter=","))
    for each in emotionData:
        is1 = False
        for e in each:
            if e == '1':
                is1 = True
        if(is1):
            cleanEmotions.append(each)
    return np.array(cleanEmotions)

def processText(book, emotions):
    replaceCharsEmpty = ['{','}','(',')','[',']','"',',','\'']
    replaceCharsSpace = ['\n','\r','\\','-']
    replaceCharsDot = ['!','?',':',';']
    book = book.lower()
    for each in replaceCharsEmpty:
        book = book.replace(each,'')
    for each in replaceCharsSpace:
        book = book.replace(each,' ')
    for each in replaceCharsDot:
        book = book.replace(each,'.')
    bookE = getEmotionWords(book, emotions)
    emotionalWordsCounter = Counter(bookE)
    return emotionalWordsCounter

def getEmotionWords(book, emotions):
    newBook = []
    book = book.split()
    for word in book:
        if word in emotions:
            newBook.append(word)
    return newBook

def getBook(directory, book, emotions):
    opened = open(directory + book, "r")
    bookTXT = opened.read()
    opened.close()
    bookClean = processText(bookTXT, emotions)
    return np.array(list(bookClean.items()))

def getEmotions(book, emotions):
    newThingy = [0,0,0,0,0,0,0,0,0,0]
    for each in book:
        for e in emotions:
            if each[0] == e[0]:
                theList = e.tolist()
                for i in range(1, len(theList)):
                    newThingy[i - 1] += int(theList[i])
                break
    return newThingy

def stripEmotion(fileName):
    emotionDict = {"positive" : 0, "negative" : 1, "anger" : 2, "anticipation" : 3, "disgust" : 4, "fear" : 5, "joy" : 6, "sadness" : 7, "surprise" : 8, "trust" : 9}
    fileName = fileName.split('_')
    fileName = fileName[1].split('.')
    return emotionDict.get(fileName[0])

def getDataReady(addy, emotions):
    allWords = []
    x = []
    y = []
    if(len(addy.split('.')) > 1):
        tmp = getBook("", addy, emotions)
        allWords.append(tmp)
        x.append(getEmotions(tmp, emotions))
        return allWords, x, []

    lsDir = os.listdir(addy)
    for each in lsDir:
        y.append(stripEmotion(each))
        tmp = getBook(addy, each, emotions)
        allWords.append(tmp)
        x.append(getEmotions(tmp, emotions))
    return allWords, x, y

def training(x, y, test_ratio):
    np.random.seed(42)
    shuffled_indices = np.random.permutation(len(x))
    test_set_size = int(len(x) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    x_train = [x[i] for i in train_indices]
    y_train = [y[i] for i in train_indices]
    x_test = [x[i] for i in test_indices]
    y_test = [y[i] for i in test_indices]
    return np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test)

def plot_precision_recall_vs_threshold(precisions, recalls, thresholds):
    plt.plot(thresholds, precisions[:-1], "b--", label="Precision")
    plt.plot(thresholds, recalls[:-1], "g-", label="Recall")
    plt.xlabel("Threshold")
    plt.legend(loc="center left")
    plt.ylim([0, 1])

def fuzzy(y, x):
    for i in range(len(y)):
        theMax = max(x[i])
        print("The texts emotion was labeled %s" % (tenEmotions[y[i]]))
        print("The top emotion was %s" % (tenEmotions[x[i].index(theMax)]))
        print("Below is the percentages of each emotion")
        if theMax == 0:
            theMax = 1
        a = [x[i][j] / theMax for j in range(len(x[i]))]
        print("  Positive Negative Anger    Anticip  Disgust   Fear      Joy     Sadness  Surprise  Trust")
        for j in range(len(a)):
            print("%8.2f" % (a[j] * 100), end=" ")
        print()
        print()

def negVSpos(x, y):
    newX = [x[i][0] for i in range(len(x))]
    newY = [x[i][1] for i in range(len(x))]

    plt.plot(newX, newY, "go")
    plt.show()

def decTree(x, y, emotions):
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(x, y)

    print("\nLoading Alice in Wonderland")
    a, xNew, yNew = getDataReady("books1/alice.txt", emotions)
    print(clf.predict_proba(xNew))

def main():
    if(len(sys.argv) != 2):
        print("Usage: python3 bookEmotion.py name_of_book.txt\nOr: python3 bookEmotion.py name_of_folder/")
        sys.exit()

    emotions = load_emotion_data('NRCcsvEmotion.csv')
    allWords, x, y = getDataReady(sys.argv[1], emotions)
    x_train, y_train, x_test, y_test = training(x, y, .4)

    y_train_Sur = (y_train == 8)
    y_test_Sur = (y_test == 8)
    sgd_clf = SGDClassifier(max_iter=1000, tol=1e-3)
    sgd_clf.fit(x_train, y_train_Sur)

    # Predictions
    #############
    #for i in range(len(x_train)):
    #    para = x_train[i]
    #    print(y_train[i])
    #    print(sgd_clf.predict([para]))

    # Cross Validation
    ##################
    print("\nCross Validation")
    print(cross_val_score(sgd_clf, x_train, y_train_Sur, cv=3, scoring="accuracy"))

    # BaseEstimator and Never8Classifier
    ####################################
    never8Class = Never8Classifier()
    print("\nBaseEstimator and Never8Classifier")
    print(cross_val_score(never8Class, x_train, y_train_Sur, cv=3, scoring="accuracy"))

    # Confusion Matrix
    ##################
    y_train_pred = cross_val_predict(sgd_clf, x_train, y_train_Sur, cv=3)
    print("\nConfusion Matrix")
    print(confusion_matrix(y_train_Sur, y_train_pred))

    # Precision and Recall
    ######################

    print("\nPrecision: %.2f" % (precision_score(y_train_Sur, y_train_pred)))
    print("Recall: %.2f" % (recall_score(y_train_Sur, y_train_pred)))

    # F1 Score
    ##########

    print("\nF1 Score: %.2f" % (f1_score(y_train_Sur, y_train_pred)))

    # Threshold Curve
    #################
    y_scores = cross_val_predict(sgd_clf, x_train, y_train_Sur, cv=3, method="decision_function")

    precisions, recalls, thresholds = precision_recall_curve(y_train_Sur, y_scores)
    #plot_precision_recall_vs_threshold(precisions, recalls, thresholds)
    #plt.show()

    # Fuzzy Logic
    #############
    #fuzzy(y, x)

    # The Normal Equation
    #####################
    x_b = np.c_[np.ones((len(x), 1)), x]
    theta_best = np.linalg.inv(x_b.T.dot(x_b)).dot(x_b.T).dot(y)
    print("\nTheta Best")
    print(theta_best)

    # PyPlot
    ########
    #plt.plot(x_train,y_train_Sur,'ro')
    #plt.show()

    # Logistic Regression Model
    ###########################
    #log_reg = LogisticRegression(solver='lbfgs', multi_class='auto')
    #log_reg.fit(x,y)
    #x_new = np.linspace(0,3,1000).reshape(-1,10)
    #y_proba = log_reg.predict_proba(x_new)
    #plt.plot(x_new, y_proba[:, 1], "g-", label="yes")
    #plt.plot(x_new, y_proba[:, 0], "b--", label="no")
    #plt.show()

    #negVSpos(x, y)

    decTree(x, y, emotions)

if __name__ == "__main__":
    main()
