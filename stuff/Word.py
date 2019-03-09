from __future__ import print_function
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('averaged_perceptron_tagger')

# NLTK Word Types:
    # Adjective = JJ
    # Adjective, comparative = JJR
    # Adjective, superlative = JJS
    # Noun, singular or mass = NN
    # Noun, plural = NNS
    # Adverb = RB
    # Adverb, comparative = RBR
    # Adverb, superlative = RBS
    # Verb, base form = VB
    # Verb, past tense = VBD
    # Verb, non-3rd person singular present = VBP
wordTypesNLTK = ["JJ", "JJR", "NN", "NNS", "RB", "RBR", "RBS", "VB", "VBD", "VBP"]

class Word:

    def __init__(self, word, sentence):
        self.word = word
        self.count = 1
        self.repetition = 1
        self.wordsAssociated = []
        self.sentenceWords(sentence)

    # My idea: This is the number of total times this color has appeared in the text divided by the total number of colors found. How often is it used and maybe that should change importance?
    def repeat(self, total):
        self.count += 1
        print(total)
        self.repetition = self.count / total

    def sentenceWords(self, sentence):
        mainWordLocation = sentence.index(self.word)
        sentence = nltk.pos_tag(sentence)

        for word in sentence:
            if word[0] not in self.wordsAssociated and word[1] in wordTypesNLTK and word[0] != self.word:
                self.wordsAssociated.append([word[0], abs(sentence.index(word) - mainWordLocation), 1])
            elif word[0] != self.word and word[1] in wordTypesNLTK:
                for w in self.wordsAssociated:
                    if w == word[0]:
                        w[2] += 1
                        w[1] = (w[1] + (sentence.index(word) - mainWordLocation)) / w[2]
