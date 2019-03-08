import os
import sys
import csv
import numpy as np
from collections import Counter
from sklearn.linear_model import SGDClassifier
from sklearn import linear_model

tenEmotions = ["Positive", "Negative", "Anger", "Anticipation", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust"]

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
        return allWords, x

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
    print(y_train)
    print(y_test)
    return np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test)

def main():
    if(len(sys.argv) != 2):
        print("Usage: python3 bookEmotion.py name_of_book.txt\nOr: python3 bookEmotion.py name_of_folder/")
        sys.exit()

    emotions = load_emotion_data('NRCcsvEmotion.csv')
    allWords, x, y = getDataReady(sys.argv[1], emotions)
    x_train, y_train, x_test, y_test = training(x, y, .3)

    y_train_Sur = (y_train == 4)
    y_test_Sur = (y_test == 4)
    sgd_clf = SGDClassifier(max_iter=1000, tol=1e-3)
    sgd_clf.fit(x_train, y_train_Sur)

    for i in range(len(x_train)):
        para = x_train[i]
        print(y_train[i])
        print(sgd_clf.predict([para]))

if __name__ == "__main__":
    main()
