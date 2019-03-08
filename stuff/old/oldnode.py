
class color:
    def __init__(self, theColor, theWords):
        self.color = theColor
        self.words = theWords
        self.totalWords = len(theWords)
        self.colorLoc = theWords.index(theColor)
        self.wordsAndWeights = []
        self.wordWeight()

    def wordWeight(self):
        # word if distance is not less than 0 -> 5
        # each word will have weight to color and percentage of times word appears
        # and how many times it appears
        for word in self.words:
            if self.words and word not in self.words:
                self.wordAndWeights.append([word, ])

    def colorAgain(self, theColor, theWords):
        newColorLoc = theWords.index(theColor)
        self.colorLoc = (self.colorLoc + newColorLoc) / 2
        for word in theWords:
            if word in self.words:
                for each in self.wordsAndWeights:
                    if word in each:
                        each[1] = (each[1] + abs(theWords.index(word) - newColorLoc)) / 2
            else:
                self.wordsAndWeights.append([word, abs(theWords.index(word) - newColorLoc)])

    def getColorLoc(self):
        print self.colorLoc

    def printSome(self):
        for each in self.wordsAndWeights:
            for word in each:
                print word
