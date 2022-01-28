"""
Language Modeling Project
Name:
Roll No:
"""

from re import L
from tracemalloc import start
from turtle import st
import language_tests as test

project = "Language" # don't edit this

### WEEK 1 ###

'''
loadBook(filename)
#1 [Check6-1]
Parameters: str
Returns: 2D list of strs
'''
def loadBook(filename):
    f = open(filename,'r')
    Lines = f.readlines()
    text=[]
    for Line in Lines:
        Line1=Line.split(" ")
        Line1[-1] = Line1[-1].strip()
        if Line1!=['']:
            text.append(Line1)   
    return text

'''
getCorpusLength(corpus)
#2 [Check6-1]
Parameters: 2D list of strs
Returns: int
'''
def getCorpusLength(corpus):
    count=0
    for statement in corpus:
        count=count+len(statement)
    return count


'''
buildVocabulary(corpus)
#3 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def buildVocabulary(corpus):
    vocab=[]
    for statement in corpus:
        for word in statement:
            if word not in vocab:
                vocab.append(word)
    return vocab


'''
countUnigrams(corpus)
#4 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countUnigrams(corpus):
    dict={}
    vocab=[]
    for statement in corpus:
        for word in statement:
            if word not in vocab:
                vocab.append(word) # unique words
    for i in range(0,len(vocab)):
                dict[vocab[i]] = 0
    for word in vocab:
        for statement in corpus:
            for word1 in statement:
                if word == word1:
                    dict[word]=dict[word]+1
    return dict

'''
getStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def getStartWords(corpus):
    start=[]
    for statement in corpus:
        if statement[0] not in start:
            start.append(statement[0])
    return start


'''
countStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countStartWords(corpus):
    allstart=[]
    start=[]
    dict={}
    for statement in corpus:
        allstart.append(statement[0])
        if statement[0] not in start:
            start.append(statement[0])
    for i in range(0,len(start)):
                    dict[start[i]] = 0
    for word in start:
        for word1 in allstart:
            if word == word1:
                dict[word]=dict[word]+1
    return dict


'''
countBigrams(corpus)
#6 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def countBigrams(corpus):
    dict={}
    for statement in corpus:
        for i in range(0, len(statement)-1):
            A=statement[i]
            if A not in dict.keys():
                dict[A]={}
                if statement[i+1] not in dict[A].keys():
                    dict[A][statement[i+1]]=1
            elif statement[i+1] in dict[A].keys():
                dict[A][statement[i + 1]] = dict[A][statement[i+1]]+1


            elif A in dict.keys():
                if statement[i + 1] not in dict[A].keys():
                    dict[A][statement[i + 1]] = 1
                elif statement[i + 1] in dict[A].keys():
                    dict[A][statement[i + 1]] = dict[A][statement[i + 1]] + 1

    return dict


### WEEK 2 ###

'''
buildUniformProbs(unigrams)
#1 [Check6-2]
Parameters: list of strs
Returns: list of floats
'''
def buildUniformProbs(unigrams):
    A=len(unigrams)
    p1=[]
    k=1/A
    for i in range(A):
        p1.append(k)

    return p1


'''
buildUnigramProbs(unigrams, unigramCounts, totalCount)
#2 [Check6-2]
Parameters: list of strs ; dict mapping strs to ints ; int
Returns: list of floats
'''
def buildUnigramProbs(unigrams, unigramCounts, totalCount):
    p1=[]
    for i in range(len(unigrams)):
        A=unigramCounts[unigrams[i]]
        B=A/totalCount
        p1.append(B)
    return p1


'''
buildBigramProbs(unigramCounts, bigramCounts)
#3 [Check6-2]
Parameters: dict mapping strs to ints ; dict mapping strs to (dicts mapping strs to ints)
Returns: dict mapping strs to (dicts mapping strs to (lists of values))
'''
def buildBigramProbs(unigramCounts, bigramCounts):
    prevWord = []
    word = []
    probs = []
    for key in bigramCounts.keys():
        prevWord.append(key)
        for key1 in bigramCounts[key].keys():
            word.append(key1)
            probs.append(bigramCounts[key][key1]/unigramCounts[key])

    dict = {}
    count=0
    for i in range(0,len(prevWord)):
        j=0
        if len(bigramCounts[prevWord[i]])==1:
            a = []
            b = []
            temp = {}
            a.append(word[count])
            temp["words"]=a
            b.append(probs[count])
            temp["probs"]=b
            dict[prevWord[i]] = temp

        elif len(bigramCounts[prevWord[i]]) > 1:
            a=[]
            b=[]
            temp={}
            for j in range(len(bigramCounts[prevWord[i]])):
                a.append(word[count+j])
                temp["words"] = a
                b.append(probs[count+j])
                temp["probs"] = b
                dict[prevWord[i]] = temp

        count=count+j+1
    return dict


'''
getTopWords(count, words, probs, ignoreList)
#4 [Check6-2]
Parameters: int ; list of strs ; list of floats ; list of strs
Returns: dict mapping strs to floats
'''
def getTopWords(count, words, probs, ignoreList):
    sortedwords=[]
    sortedprobs=[]
    for i in range(len(probs)):
        A=max(probs)
        B=probs.index(A)
        if words[B] not in ignoreList:
            sortedprobs.append(probs[B])
            sortedwords.append(words[B])
        probs[B]=0
    dict={}
    for i in range(count):
        dict[sortedwords[i]]=sortedprobs[i]

    return dict


'''
generateTextFromUnigrams(count, words, probs)
#5 [Check6-2]
Parameters: int ; list of strs ; list of floats
Returns: str
'''
from random import choices
def generateTextFromUnigrams(count, words, probs):
    lst=[]
    sentence=''
    for i in range(count):
        lst.append(choices(words, weights=probs)[0])
    for j in range(len(lst)):
        sentence=sentence+ ' '+lst[j]
    
    return sentence


'''
generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs)
#6 [Check6-2]
Parameters: int ; list of strs ; list of floats ; dict mapping strs to (dicts mapping strs to (lists of values))
Returns: str
'''
def generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs):
    return


### WEEK 3 ###

ignore = [ ",", ".", "?", "'", '"', "-", "!", ":", ";", "by", "around", "over",
           "a", "on", "be", "in", "the", "is", "on", "and", "to", "of", "it",
           "as", "an", "but", "at", "if", "so", "was", "were", "for", "this",
           "that", "onto", "from", "not", "into" ]

'''
graphTop50Words(corpus)
#3 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTop50Words(corpus):
    return


'''
graphTopStartWords(corpus)
#4 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTopStartWords(corpus):
    return


'''
graphTopNextWords(corpus, word)
#5 [Hw6]
Parameters: 2D list of strs ; str
Returns: None
'''
def graphTopNextWords(corpus, word):
    return


'''
setupChartData(corpus1, corpus2, topWordCount)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int
Returns: dict mapping strs to (lists of values)
'''
def setupChartData(corpus1, corpus2, topWordCount):
    return


'''
graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; str ; 2D list of strs ; str ; int ; str
Returns: None
'''
def graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title):
    return


'''
graphTopWordsInScatterplot(corpus1, corpus2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int ; str
Returns: None
'''
def graphTopWordsInScatterplot(corpus1, corpus2, numWords, title):
    return


### WEEK 3 PROVIDED CODE ###

"""
Expects a dictionary of words as keys with probabilities as values, and a title
Plots the words on the x axis, probabilities as the y axis and puts a title on top.
"""
def barPlot(dict, title):
    import matplotlib.pyplot as plt

    names = []
    values = []
    for k in dict:
        names.append(k)
        values.append(dict[k])

    plt.bar(names, values)

    plt.xticks(rotation='vertical')
    plt.title(title)

    plt.show()

"""
Expects 3 lists - one of x values, and two of values such that the index of a name
corresponds to a value at the same index in both lists. Category1 and Category2
are the labels for the different colors in the graph. For example, you may use
it to graph two categories of probabilities side by side to look at the differences.
"""
def sideBySideBarPlots(xValues, values1, values2, category1, category2, title):
    import matplotlib.pyplot as plt

    w = 0.35  # the width of the bars

    plt.bar(xValues, values1, width=-w, align='edge', label=category1)
    plt.bar(xValues, values2, width= w, align='edge', label=category2)

    plt.xticks(rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Note that this limits the graph to go from 0x0 to 0.02 x 0.02.
"""
def scatterPlot(xs, ys, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xs, ys)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xs[i], ys[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.xlim(0, 0.02)
    plt.ylim(0, 0.02)

    # a bit of advanced code to draw a y=x line
    ax.plot([0, 1], [0, 1], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    test.week1Tests()
    print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    test.runWeek1()

    ## Uncomment these for Week 2 ##

    print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()
    print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    test.runWeek2()


    ## Uncomment these for Week 3 ##
"""
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()
"""