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
Here I introduce a approach to anlyse the time(chapter)-series sentiment relation between character in War and Peace book one. The relation between characters could change along the story. Lovers may become haters. I use [Named Entity Recognizer](https://nlp.stanford.edu/software/CRF-NER.shtml) of Stanford NLP Group to identify characters and locations. And based on the ntlk's [Sentiment Intensity Analyzer](https://www.nltk.org/api/nltk.sentiment.html), we can calculate the sentiment score of content of two characters. In the end we can see how those scores change in different chapters. Also we try Textrank for text summarization and RNN for text generation.<br />
Time is really short and I have no powerful laptop. It is difficult to get a ideal result from the training. But I show the direction towards to the target.


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
Same reason as the previous task, I have no labeled data for sentiments of this book. So I use the pre-trained model from NTLK. This library can caculate a sentiment score of given text. We could use this to identify sentiments of sentences or chapters. But since we have already indenfied all characters‘ name , we can know the sentiment between them. We define two characters are connected if they are mentioned within two sentences. We calculate the average sentiment score of nearby (3) sentences, we use the average score as the sentiments of this relation.
```
It is raining                    # sentiment score 0
"I hate you !" said by Natasha.  # sentiment score -0.5  Natasha is mentioned
"And I Love Pierre"              # sentiment score 0.8  Pierre is mentioned
```
The final score of this conversaion is ( 0.8-0.5 )/3 = 0.1. Natasha and Pierre get 0.1 point for thier relation here.<br />
<br />
And normally the attitude between characters can change with the development of the story. So we compare all the sentiment score with time.<br />
### how to run
```
* run sentiments.py

```
### results
I use the main character Pierre as test.  The best character to him is Mary Bolkonskaya and worst is Dolokhov. They will have some drama in other chapters following. It makes sence they have a bad relation. The most frequent mentioned togather character is Prince Anatole.<br />
From the figure you can see Dolokhov and Pierre have a not so pleasure experience in chapter 9. They meet in a bar and Dolokhov try to bet with a Englishman . And they have no connecation after that. And sentiment score of Prince Anatole keeps changing in different chapters.<br />
![figure](https://github.com/licheng5625/data-science-task/blob/master/result.png) )

### limitations
I did not read the book before. I cannot explain what happened causes the sentiment score increasing or decreasing........(although I watched the TV show)

The story is too short to describe all the characters. Their story is still going on. It would be interesting to add following chapters and to see if the sentiment between Helene and Pierre rises up in their wedding and falls down to negative .<br />

We only caculate 3 sentences around the characters but those contents might not be relevent to those characters or there are more sentences about them following. We should caculate the score per event between two characters. Then we need event detection etc.<br />
We didn't consider the different weights of sentiment in different chapter - a fading model. The sentiment score of chapter 1 should not be same value as current chapter. We could add more weight for near chapter and ignore the sentiment score from far far ealier chapters<br />

## Summarize paragraphs
I knew a algorithm for summarizing text when I did master thesis. It called [Textrank]( https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf). It is similar to pagerank. So it is graphbased algorithm and do not need to train<br />

### how to run
```
* put the articles into Textrank/articles

* run textrank.py

```
I knew another model which could do this task. It is called [FastText](https://github.com/facebookresearch/fastText/tree/master/python). I used this in my master thesis, but the result is not so good. The advantage of this model is you can fast train.
### results
[here](https://github.com/licheng5625/data-science-task/tree/master/TextRank/summaries)


## Text Gereration
 We could train a RNN model to gererate text to simulate Leo Tolstoy. First I try a single layer RNN, after 20 epochs accuracy is stable around 0.022. Source code refences to Jason Brownlee's [blog](https://machinelearningmastery.com/text-generation-lstm-recurrent-neural-networks-python-keras/). I use a sentence from chapter 4 for testing.
 ```
 
 Seed:
 "andre," said his wife, addressing her husband in the same coquettish manner in which she spoke to Original:
 ther men, "the vicomte has been telling us such a tale about Mademoiselle George and Buonaparte!"
 ```
```
 acc: 0.2245  - val_acc: 0.2073
 Result 1 layer Rnn with text from chapter 1 for training:
 er  an  an whe  aa toe  aad  ah  an whe  aa tou  aad  ah  an whe  aa tou  aad  ah  an  hh thu  aa tou  aad  ah  an whe  aa tou  aad  ah  an  hh thu  aa tou  aad  ah  an whe  aa tou  aad  ah  an  hh thu  aa tou  aad  ah  an whe  aa tou  aad  ah  an  hh thu  aa tou  aad  ah  an whe  aa tou  aad  ah  an  hh thu  aa tou  aad  ah  an whe  aa tou  aad  ah  an  hh thu  aa tou  aad  ah  an whe  aa tou  aad
 
 Result 2 layer Rnn with text from chapter 1-3 for training:
 ent the gopdror. and the sigled to the cuc d'enghien had been edcimed to the cuc d'enghien had been rectmedd to his face of the conversation of the eeae and and she sic buc d'enghien had been rectmedd to his face of the conversation of the eeae ootioe orincess had beenmi wou as the soom as the sooke thi abbe another dnd not one of the soom as the sooke man with a prince and secllnende to the goperor. and the sic bbbe and prersiog his face of the eoneror. and the sic bbbe and prersing his face of the eoneror. and the sic bbbe and prersing his face of the eoneror. and the sic bbbe and prersing his face of the eoneror.

 ```
 The text of result 1 is just repeating itself. We can use more layers or more train data. So I try agin with 2 layer LSTM ,but I have no GPU laptop. It is still running 12:30 30.Nov.<br />
 12.1 UPDATE  I get a accuracy 56% 2 layer Rnn model. I show the result above. There are some english words already, but the whole sentence still has no sence. I think with a bigger data and more time. The result could be better.(at least after 20 epochs , the model does still not converge )


 
