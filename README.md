# Data Science Task

Here is the project which I did for data science task interview
The tasks are :
    Word and phrase distribution.
    Identify all the places and characters in the book.
    Identify sentiments of the different sentences and chapters.
    Summarize paragraphs.
    Extract intents from sentences.
    Track key concepts throughout the book.
The data source is [<War and Peace book one>](https://en.wikisource.org/wiki/War_and_Peace/Book_One) .

## Abstract
Here I introduce a approach to anlyse the time(chapter)-series sentiment relation between character in War and Peace book one. The relation between characters could change along the story. Lovers may become haters. I use [Named Entity Recognizer] (https://nlp.stanford.edu/software/CRF-NER.shtml) of Stanford NLP Group to identify characters and locations. And based on the ntlk's [Sentiment Intensity Analyzer](https://www.nltk.org/api/nltk.sentiment.html), we can calculate the sentiment score of content of two characters. In the end we can see how those scores change in different chapters.


## Identify the places and characters

This is a named entity recognition task. It could use supervised data to train a recognizer for this book. But I need a ladeled text for training. And there are papers about "unsupervised" named entity recognition. But we still need some seeds and the dataset might be not big engough to do so (I didn't try). So I used a pre-trained recognizer from Stanford with 3 class dimension .
### how to run

 * run getCharacters.py
 * you will get two lists --- characters' fullname and locations



### results
Total 129 [fullnames](https://github.com/licheng5625/data-science-task/blob/master/characts.txt) and 51 [locations](https://github.com/licheng5625/data-science-task/blob/master/locations.txt) are extracted.
I checked some of them in [wiki](https://en.wikipedia.org/wiki/List_of_War_and_Peace_characters). Most of them you can find in that wiki or you can some results from google with name and "war and peace" as key word.

### limitations
There are still some funny characters like Mimi which is actrully the doll of natasha or Andrusha which is a pet name.
And Anna Pavlovna Scherer and Annette Scherer are the same person, the model is failed to identify that.

## Identify sentiments between different characters
Same reason as the previous task, I have no labeled data for sentiments of this book. So I use the pre-trained model from NTLK. This libiray can caculate a sentiment score of given text. We could use this to identify sentiments of sentences or chapters. But since we have already indenfied all characters, we can know the sentiment between them. We define two characters are connected if they are mentioned within two sentences. We calculate the sentiment score of nearby (3) sentences, we use the average score as the sentiments of this relation.
```
It is raining                    # sentiment score 0
"I hate you !" said by Natasha.  # sentiment score -0.5  Natasha is mentioned
"And I Love Pierre"              # sentiment score 0.8  Pierre is mentioned
```
The final score of the conversaion is ( 0.8-0.5 )/3 = 0.1. Natasha and Pierre get 0.1 point for thier relation here.

And nomally the attitude between characters can change with the development of the story. So we compare all the sentiment score with time.

### how to run
```
* run sentiments.py

```
### results
I use the main character Pierre as test.  The best character to him is Mary Bolkonskaya and worst is Dolokhov. They will have some drama in other chapters following. The most frequent mentioned togather character is Prince Anatole.
From the figure you can see Dolokhov meet Pierre in a bar in chapter 9. And they have no connecation after that. And sentiment score of Prince Anatole keeps changing in different chapters.
![figure](https://github.com/licheng5625/data-science-task/blob/master/result.png) )

### limitations


## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

