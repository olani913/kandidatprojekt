# -*- coding: cp1252 -*-
import os
from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier

newsTrainer = Trainer(tokenizer)

# You need to train the system passing each text one by one to the trainer module.


#newsSet =[
#    {'text': 'not to eat too much is not enough to lose weight', 'category': 'health'},
#    {'text': 'Russia try to invade Ukraine', 'category': 'politics'},
#    {'text': 'do not neglect exercise', 'category': 'health'},
#    {'text': 'Syria is the main issue, Obama says', 'category': 'politics'},
#    {'text': 'eat to lose weight', 'category': 'health'},
#    {'text': 'you should not eat much', 'category': 'health'}
#]

#testSet.append({'text': 'DETTA KONNER EJ MED', 'category': 'health'})



#news=open(file_path_and_name,"r")

trainingSet=[]
#training with fake news
path = './data/news/training_fake/'
for filename in os.listdir(path):
    file_path_and_name=path+filename
    news=open(file_path_and_name,"r")
    read = news.read()
    trainingSet.append({"text":read,'category': 'fakeNews'})  
    print("de filnamn som h�r till fakenews �r: " +filename)

#training with real news
path = './data/news/training_real/'    
for filename in os.listdir(path):
    file_path_and_name=path+filename
    news=open(file_path_and_name,"r")
    read=news.read()
    trainingSet.append({"text":read ,'category': 'realNews'})  
    print("de filnamn som �r de riktiga nyheterna �r: " +filename) 
    



for news in trainingSet:
    newsTrainer.train(news['text'], news['category'])


# When you have sufficient trained data, you are almost done and can start to use
# a classifier.
newsClassifier = Classifier(newsTrainer.data, tokenizer)

# Now you have a classifier which can give a try to classifiy text of news whose
# category is unknown, yet.
testSet=[]
path = './data/news/LinksUnknownClass/' 
for filename in os.listdir(path):
    file_path_and_name=path+filename
    news=open(file_path_and_name,"r")
    read=news.read()
    classification = newsClassifier.classify(read)
    print str(classification) + ' ' + filename

# the classification variable holds the detected categories sorted

