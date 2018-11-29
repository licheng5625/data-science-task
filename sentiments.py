import os
import copy

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

def extractChar(characts,charactsfullnameMap,text):
    char = set()
    for w in characts:
        if w in text:
            char.add(charactsfullnameMap[w])
    return char


sid = SentimentIntensityAnalyzer()
characts= set()
charactsFullName= set()
characts2FullName = {}
descrptionOfText = {'sentiment':0 , 'characts': set() }
relationGraph = { }
relationGraphlist=[]
with open('characts.txt', mode='r') as reader:
    for char in reader:
        charactsFullName.add(char.replace('\n',''))

with open('charactsWithoutMerging.txt', mode='r') as reader:
    for char in reader:
        char = char.replace('\n','')
        characts.add(char)
        for fullname in  charactsFullName:
            fullnameFlag = True
            for name in char.split():
                if name not in fullname.split():
                    fullnameFlag = False
                    break
            if fullnameFlag :
                characts2FullName[char] = fullname
                break
# loading the characts' name and their fullnames
for charact in charactsFullName:
    intiGraph ={}
    for to_charact in charactsFullName:
        intiGraph[to_charact]={'times':0 , 'Sentiment':0}
    relationGraph[charact]=intiGraph

list_dirs = os.walk('./CHAPTERS')
for root, dirs, files in list_dirs:
    # loop in all chapters

    files.sort()
    for file in files:
        if ('.txt' not in file)  :
            continue

        text=[]
        with open('./CHAPTERS/'+file, mode='r') as reader:
            for line in reader:
                if line != '\n':
                    text.append(line)

        InfoOfLine = [{'sentiment':0 , 'characts': set() } for n in range(len(text))]



        for lineNum in range(len(text)):
            # get characts' name in this line

            char = extractChar(characts,characts2FullName,text[lineNum])
             # if there is a characts's name shows up,
             # we caculate the sentiment score of this line and the line previous and following

            if len(char) is not 0:
                InfoOfLine[lineNum]['characts']=char
                InfoOfLine[lineNum]['sentiment']=sid.polarity_scores(text[lineNum])['compound']
                if lineNum +1 < len(text):
                    InfoOfLine[lineNum+1]['sentiment']=sid.polarity_scores(text[lineNum+1])['compound']
                    InfoOfLine[lineNum-1]['sentiment']=sid.polarity_scores(text[lineNum-1])['compound']
        # if the there is a charact and there is other characts show up nearby(one line after)
        # it means there is a relationship between them
        # I caculate the average sentiment score to this relationship
        for infoOfEachLine in range(len(InfoOfLine)):
            if infoOfEachLine == 0:
                allChars = InfoOfLine[infoOfEachLine]['characts'] | InfoOfLine[infoOfEachLine+1]['characts']
                meanSentiment = (InfoOfLine[infoOfEachLine]['sentiment'] + InfoOfLine[infoOfEachLine+1]['sentiment'])/2
            if infoOfEachLine == len(InfoOfLine)-1:
                allChars = InfoOfLine[infoOfEachLine]['characts'] | InfoOfLine[infoOfEachLine-1]['characts']
                meanSentiment = (InfoOfLine[infoOfEachLine]['sentiment'] + InfoOfLine[infoOfEachLine-1]['sentiment'])/2
            if infoOfEachLine != len(InfoOfLine)-1 and infoOfEachLine != 0:
                allChars = InfoOfLine[infoOfEachLine]['characts'] | InfoOfLine[infoOfEachLine-1]['characts'] | InfoOfLine[infoOfEachLine+1]['characts']
                meanSentiment = (InfoOfLine[infoOfEachLine]['sentiment'] + InfoOfLine[infoOfEachLine-1]['sentiment'] + InfoOfLine[infoOfEachLine+1]['sentiment'])/3

            if len(allChars)>1:
                for charact in allChars:
                    for to_charact in allChars:
                        if charact == to_charact:
                            continue
                        relationGraph[charact][to_charact]['times']+=1
                        relationGraph[charact][to_charact]['Sentiment']+=meanSentiment
        relationGraphThisChapter = copy.deepcopy(relationGraph)
        for relCharacts in relationGraphThisChapter.keys():
            for to_characts in relationGraphThisChapter[relCharacts].keys():
                if relationGraphThisChapter[relCharacts][to_characts]['times']!=0:
                    relationGraphThisChapter[relCharacts][to_characts]['MeanSentiment'] = relationGraphThisChapter[relCharacts][to_characts]['Sentiment']/relationGraphThisChapter[relCharacts][to_characts]['times']
                else:
                    relationGraphThisChapter[relCharacts][to_characts]['MeanSentiment'] =  0
        relationGraphlist.append(relationGraphThisChapter)
# As a result we can see a time series sentiment scores between two characts
for relation in relationGraphlist:
        print(relation['Monsieur Pierre']['Natasha'])

