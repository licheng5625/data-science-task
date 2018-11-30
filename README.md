# Data Science Task

Here is the project which I did for data science task interview<br />
The tasks are :<br />
   &nbsp; &nbsp; Word and phrase distribution.<br />
    &nbsp; &nbsp; Identify all the places and characters in the book.<br />
    &nbsp; &nbsp; Identify sentiments of the different sentences and chapters.<br />
    &nbsp; &nbsp; Summarize paragraphs.<br />
    &nbsp; &nbsp; Extract intents from sentences.<br />
    &nbsp; &nbsp; Track key concepts throughout the book.<br />
The data source is [<War and Peace book one>](https://en.wikisource.org/wiki/War_and_Peace/Book_One) .

## Abstract
Here I introduce a approach to anlyse the time(chapter)-series sentiment relation between character in War and Peace book one. The relation between characters could change along the story. Lovers may become haters. I use [Named Entity Recognizer](https://nlp.stanford.edu/software/CRF-NER.shtml) of Stanford NLP Group to identify characters and locations. And based on the ntlk's [Sentiment Intensity Analyzer](https://www.nltk.org/api/nltk.sentiment.html), we can calculate the sentiment score of content of two characters. In the end we can see how those scores change in different chapters.


## Identify the places and characters

This is a named entity recognition task. It could use supervised data to train a recognizer for this book. But I need a ladeled text for training. And there are papers about "unsupervised" named entity recognition. But we still need some seeds and the dataset might be not big engough to do so (I didn't try). So I used a pre-trained recognizer from Stanford with 3 class dimension .
### how to run
```
* run getCharacters.py
* you will get two lists --- characters' fullname and locations
 ```



### results
Total 129 [fullnames](https://github.com/licheng5625/data-science-task/blob/master/characts.txt) and 51 [locations](https://github.com/licheng5625/data-science-task/blob/master/locations.txt) are extracted.<br />
I checked some of them in [wiki](https://en.wikipedia.org/wiki/List_of_War_and_Peace_characters). Most of them can be found in that wiki or you can get some results from google with name and "war and peace" as key word.<br />

### limitations
There are still some funny characters like Mimi which is actrully the doll of Natasha or Andrusha which is a pet name.
And Anna Pavlovna Scherer and Annette Scherer are the same person, the model is failed to identify that.

## Identify sentiments between different characters
Same reason as the previous task, I have no labeled data for sentiments of this book. So I use the pre-trained model from NTLK. This libiray can caculate a sentiment score of given text. We could use this to identify sentiments of sentences or chapters. But since we have already indenfied all characters, we can know the sentiment between them. We define two characters are connected if they are mentioned within two sentences. We calculate the sentiment score of nearby (3) sentences, we use the average score as the sentiments of this relation.
```
It is raining                    # sentiment score 0
"I hate you !" said by Natasha.  # sentiment score -0.5  Natasha is mentioned
"And I Love Pierre"              # sentiment score 0.8  Pierre is mentioned
```
The final score of the conversaion is ( 0.8-0.5 )/3 = 0.1. Natasha and Pierre get 0.1 point for thier relation here.<br />
<br />
And nomally the attitude between characters can change with the development of the story. So we compare all the sentiment score with time.<br />

### how to run
```
* run sentiments.py

```
### results
I use the main character Pierre as test.  The best character to him is Mary Bolkonskaya and worst is Dolokhov. They will have some drama in other chapters following. The most frequent mentioned togather character is Prince Anatole.<br />
From the figure you can see Dolokhov and Pierre have a not so pleasure experience in chapter 9. They meet in a bar and Dolokhov try to bet a Englishman . And they have no connecation after that. And sentiment score of Prince Anatole keeps changing in different chapters.<br />
![figure](https://github.com/licheng5625/data-science-task/blob/master/result.png) )

### limitations
I did not read the book before. I cannot explain what happened causes the sentiment score increasing or decreasing........(I watched the TV show though)

The story is too short to describe all the characters. Their story is still going on. It would be interesting to add following chapters and to see if the sentiment between Helene and Pierre rises up and falls down to negative .<br />

We only caculate 3 sentences around the characters but those contents might not be relevent to those characters or there are more sentences following. We should caculate the score per event between two characters. Then we need event detection etc.<br />
We didn't consider the different weights of sentiment in different chapter - a fading model. The sentiment score of chapter 1 should not be same value as current chapter. We could add more weight for near chapter and ignore the sentiment score from far far ealier chapters<br />

## Summarize paragraphs
I knew a algorithm for summarizing text when I did master thesis. It called [Textrank]( https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf). It is similar to pagerank. So it is graphbased algorithm and do not need to train<br />

### how to run
```
* put the articles into Textrank/articles

* run textrank.py

```
### results
[here](https://github.com/licheng5625/data-science-task/tree/master/TextRank/summaries)


## Text Gereration
 We could train a RNN model to gererate text to simulate Leo Tolstoy. First I try a single layer RNN, after 20 epochs loss is stable around 0.0789. Source code refences to Jason Brownlee's [blog](https://machinelearningmastery.com/text-generation-lstm-recurrent-neural-networks-python-keras/).
 ```
 Seed:
 " " he said at last. "you know i did all a father could for their education, and they have both turned "
 Result:
 "aa the  aoe  ao woe  ao woe  ao  an ah the  ao woe  ao  an ah the  ao woe
 ```
 The text are repeating itself. We can use more layers or more train data. So I try agin with 2 layer LSTM ,but I have no GPU laptop. It is still running 12:30 30.Nov.
 