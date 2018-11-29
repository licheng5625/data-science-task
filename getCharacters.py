import os
from nltk.tag import StanfordNERTagger
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
st = StanfordNERTagger(model_filename = './stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz', path_to_jar= './stanford-ner-2018-10-16/stanford-ner.jar' )
characts= set()
location= set()
with open('War and Peace_Book One.txt', mode='r') as reader:
    data=reader.read()
    firstName = ''
    firstLocaltion = ''
    stopWords = set(stopwords.words('english'))
    words = word_tokenize(data)
    wordsFiltered = []
    data= data.replace('.',' . ').replace(',',' , ').replace("'s"," 's ").replace('-',' - ').replace('?',' ? ').replace('!',' ! ').replace("'"," ' ").replace('"',' " ').replace(':',' : ').replace('(',' ').replace(')',' ')

    data= data.replace(';',' ; ')
    data= data.replace('\n',' ; ')

    labeledWord = st.tag(data.split())
    for word in labeledWord:
        if word[1] == 'PERSON' and word[0].lower() not in ('he','she','they','we', 'him', 'her' ,'I' ,'them'):
            firstName = firstName + ' ' + word[0]
        else:
            if firstName != '':
                characts.add(firstName)
                firstName = ''
                #print(characts)
        if word[1] == 'LOCATION':
            firstLocaltion = firstLocaltion + ' ' + word[0]
        else:
            if firstLocaltion != '':
                location.add(firstLocaltion)
                firstLocaltion = ''
    if firstLocaltion != '':
        location.add(firstLocaltion)
    if firstName != '':
        characts.add(firstName)
charactsForOutput = set()

for char in characts:
    charactsForOutput.add(char)
    for charFullname in characts:
        if len(charFullname) > len(char):
            deleteFlag = True
            for charname in char.split():
                if charname not in charFullname.split():
                    deleteFlag = False
                    break
            if deleteFlag:
                charactsForOutput.remove(char)
                break

charactsForOutput = list(charactsForOutput)
characts = list(characts)
location = list(location)
charactsForOutput.sort()
location.sort()
with open('characts.txt', mode='w') as writer:
    for char in charactsForOutput:
        writer.write(char[1:] + '\n')
with open('charactsWithoutMerging.txt', mode='w') as writer:
    for char in characts:
        writer.write(char[1:] + '\n')

with open('locations.txt', mode='w') as writer:
    for loc in location:
        writer.write(loc[1:] + '\n')