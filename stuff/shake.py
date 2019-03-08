import os
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
allBooks = []
emotions = ["Positive", "Negative", "Anger", "Anticipation", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust"]
corrData = []

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

def processText(files, folder, data):
    global overallEmotions
    tmp = []
    for eachFile in files:
        location = ""
        location = folder + "/" + eachFile
        fh = open(location, "r")

        fh = fh.read()
        replaceCharsEmpty = ['{','}','(',')','[',']','"',',','\'']
        replaceCharsSpace = ['\n','\r','\\','-','\\t']
        replaceCharsDot = ['!','?',':',';']
        for each in replaceCharsEmpty:
            fh = fh.replace(each,'')
        for each in replaceCharsSpace:
            fh = fh.replace(each,' ')
        for each in replaceCharsDot:
            fh = fh.replace(each,'.')
        sentences = fh.split('. ')
        tmp.append(addEachSentence(sentences, data))

    return tmp

def addEachSentence(sentences, data):
    words = ["MENENIUS","AUFIDIUS","CORIOLANUS", "SICINIUS"]
    overallEmotions = resetEmotions()
    allParses = []
    for name in words:
        overallEmotions = resetEmotions()
        for sentence in sentences:
            sentence = sentence.split()
            sentence = list(filter(None, sentence))
            if name in sentence:
                for word in sentence:
                    try:
                        for e in emotions:
                            if data.loc[word][e] > 0:
                                overallEmotions[emotions.index(e)][1] *= corrData[emotions.index(e)][1][1]

                    except:
                        pass
        for i in range (0, len(overallEmotions)):
            overallEmotions[i] = overallEmotions[i] * 1000
        allParses.append([name, overallEmotions])

    return allParses

def load_emotion_data(name):
    return pd.read_csv(name) #, encoding='iso-8859-1')

def split_train_test(data, test_ratio):
    np.random.seed(42)
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]

def getCorrData(data):
    corr_matrix = data.corr()
    for e in emotions:
        corrData.append([e, corr_matrix[e].sort_values(ascending = False)])
    #for each in corrData:dd
    #    for e in range(0, len(each[1])):
    #        each[1][e] = (each[1][e] + 1) / 2
    print(corrData)

def main():
    # Loading emotional data
    edata = load_emotion_data('NRCcsvEmotion.csv')

    # Making a copy of it and setting the index to English
    edata2 = edata.copy()
    edata2 = edata2.set_index("English (en)")

    # Getting correlated data of the total feeling of emotions compared to others.
    getCorrData(edata2)

    # Folder with Shakespear stuff and getting the data ready
    folder = "shake"
    files = openFolder(folder)

    # Processing words and emotions
    allBooks = processText(files, folder, edata2)

    maximum = ["", 0]
    for item in allBooks:
        for i in item:
            print(i[0])
            for each in i[1]:
                if each[1] < 1:
                    if each[1] > maximum[1]:
                        maximum[1] = each[1]
                        maximum[0] = each[0]
                print("Emotion: %s and Grade: %f" % (each[0], each[1]))
            print("The maximum emotion is, %s at: %f" % (maximum[0], maximum[1]))
            maximum = ["", 0]
            print()

if __name__ == "__main__":
    main()
