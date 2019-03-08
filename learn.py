import os
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
emotions = ["Positive", "Negative", "Anger", "Anticipation", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust"]

def resetEmotions():
    overallEmotions = []
    for e in emotions:
        overallEmotions.append([e, 1])
    return overallEmotions

def openFolder(folder):
    files = []
    for root, dirs, fileNames in os.walk(folder):
        files = fileNames
    return files

def processText(files, folder, data, cd):
    tmp = []
    allWords = []
    for eachFile in files:
        location = folder + "/" + eachFile
        fh = open(location, "r")

        fh = fh.read()
        replaceCharsEmpty = ['{','}','(',')','[',']','"',',','\'']
        replaceCharsSpace = ['\n','\r','\\','-']
        replaceCharsDot = ['!','?',':',';']
        for each in replaceCharsEmpty:
            fh = fh.replace(each,'')
        for each in replaceCharsSpace:
            fh = fh.replace(each,' ')
        for each in replaceCharsDot:
            fh = fh.replace(each,'.')
        sentences = fh.split('. ')
        a, b = addEachSentence(sentences, data, cd)
        tmp.append(a)
        allWords.append(b)

    return tmp, allWords

def addEachSentence(sentences, data, cd):
    overallEmotions = resetEmotions()
    wordsCount = {}
    for sentence in sentences:
        sentence = sentence.replace('.', '')
        sentence = sentence.split(' ')
        sentence = list(filter(None, sentence))
        for word in sentence:
            try:
                for e in emotions:
                    if data.loc[word][e] > 0:
                        #newValue = (overallEmotions[emotions.index(e)][1] * cd[emotions.index(e)][1][1])
                        overallEmotions[emotions.index(e)][1] += 1
                        if(word not in wordsCount):
                            wordsCount[word] = 1
                        else:
                            wordsCount[word] += 1
            except:
                pass
    return overallEmotions, wordsCount

def load_emotion_data(name):
    return pd.read_csv(name)

def split_train_test(data, test_ratio):
    np.random.seed(42)
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]

def getCorrData(cd, data):
    corr_matrix = data.corr()
    for e in emotions:
        cd.append([e, corr_matrix[e].sort_values(ascending = False)])
    for each in cd:
        for e in range(0, len(each[1])):
            each[1][e] = (each[1][e] + 1) / 2

def main():
    corrData = []
    emotionData = load_emotion_data('NRCcsvEmotion.csv')

    emotionDataCopy = emotionData.copy()
    emotionDataCopy = emotionDataCopy.set_index("English (en)")

    # This actually finds out the emphasis of each emotion to each other. There is a varient of weight based on each emotion to each other. Since I am trying to get a fuzzy idea of what emotion a text has, I figured this may be a better way of understanding that.
    getCorrData(corrData, emotionDataCopy)

    # The location of where your txt files are
    folder = "books1"

    # This returns a list of the files to work on.
    files = openFolder(folder)

    allBooks, wordsCount = processText(files, folder, emotionDataCopy, corrData)
    s = np.array(wordsCount)
    train, test = split_train_test(s, .3)
    print(len(train))
    print(len(test))
    count = 0
    #for book in allBooks:
    #    maxFound = max(map(lambda x: x[1], book))
    #    minFound = min(map(lambda x: x[1], book))

if __name__ == "__main__":
    main()
