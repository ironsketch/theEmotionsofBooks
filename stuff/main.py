# Michelle Bergin
#
# =========================
# The idea is to parse books for words of color, find words related and give them a weight of [0,1] and eventually to give them a fuzzy rating related to an emotion based on the words around it and the word itself...

import os
from Word import Word

colors = ["green", "blue", "violet", "crimson", "alabaster", "orange", "aqua", "amaranth", "purple", "pink", "red", "amber", "bronze", "brown", "gold", "silver", "yellow", "amethyst", "white", "brass", "fuchsia", "ruby", "aquamarine", "lime", "gray", "auburn", "azure", "batorange", "beige", "black", "blond", "blood", "sapphire", "lavender", "lilac", "maroon", "turquoise", "burgundy", "cadet", "cerulean", "charcoal", "chartreuse", "copper", "coral", "cyan", "ebony", "ultramarine", "firebrick", "garnet", "ivory", "indigo", "jade", "khaki", "magenta", "mahogany", "mauve", "olive", "opal", "periwinkle", "scarlet", "sienna", "tan", "teal", "topaz", "umber", "vermillion"]

totalNumberOfColorsFound = 0

nodes = {}

def main():
    # All book text needs to go into a folder in this directory called books.
    folder = "books"

    # Walking the folder to pull out all the files therein
    files = openFolder(folder)

    # Parsing out colors from the files
    processText(files, folder)

    # A reminder how to print... sigh
    # print("Node colors %d and all colors %d" % (len(nodes), len(colors)))
    for key, value in nodes.items():
        print(value.word)
        print(value.wordsAssociated)
        print(value.repetition)
        print()

def openFolder(folder):
    files = []
    for root, dirs, fileNames in os.walk(folder):
        files = fileNames
    return files

def processText(files,folder):
    for eachFile in files:
        location = ""
        location = folder + "/" + eachFile
        fh = open(location, "r")

        # Reading and stripping annoying shit from my text files
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
        # Pulling out sentences from the text
        sentences = fh.split('. ')
        addEachSentence(sentences)

def addEachSentence(sentences):
    global totalNumberOfColorsFound
    for sentence in sentences:

        # Getting rid of unnecessary shit again
        sentence = sentence.replace('.', '')
        sentence = sentence.split(' ')
        sentence = list(filter(None, sentence))
        for cword in sentence:
            new = True
            # If the word in the sentance is one of the colors above:
            if cword in colors:
                totalNumberOfColorsFound += 1
                # If the color is already a node
                if cword not in nodes:
                    nodes[cword] = Word(cword, sentence)
                else:
                    nodes.get(cword).repeat(totalNumberOfColorsFound)
                    nodes.get(cword).sentenceWords(sentence)

if __name__ == '__main__':
    main()
