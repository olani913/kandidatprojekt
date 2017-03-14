# -*- coding: cp1252 -*-
##import os
##from naiveBayesClassifier import tokenizer
##from naiveBayesClassifier.trainer import Trainer
##from naiveBayesClassifier.classifier import Classifier

#newsTrainer = Trainer(tokenizer)

import os
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.pipeline import Pipeline

from pandas import DataFrame

NEWLINE = '\n'

def read_files(path):
    for root, dir_names, file_names in os.walk(path):
        for path in dir_names:
            read_files(os.path.join(root, path))
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path) and os.path.getsize(file_path) > 200L:
                lines = []
                f = open(file_path)
                for line in f:
                    lines.append(line)
                f.close()
                content = NEWLINE.join(lines)
                yield file_path, content

def build_test_frame(path):
    rows = []
    index = []
    for file_name, text in read_files(path):
        rows.append({'text': text})
        index.append(file_name)

    test_frame = DataFrame(rows, index=index)
    return test_frame

def build_data_frame(path, classification):
    rows = []
    index = []
    for file_name, text in read_files(path):
        rows.append({'text': text, 'class': classification})
        index.append(file_name)

    data_frame = DataFrame(rows, index=index)
    return data_frame

pipeline = Pipeline([
    ('vectorizer',  CountVectorizer(ngram_range=(1, 3), stop_words='english', encoding="utf-8")),
    ('classifier',  MultinomialNB()) ])

REAL = 'real'
FAKE = 'fake'

SOURCES = [
    ('./data/news/training_fake/',      FAKE),
    ('./data/news/training_real/',    REAL)
]

data = DataFrame({'text': [], 'class': []})
for path, classification in SOURCES:
    data = data.append(build_data_frame(path, classification))

data = data.reindex(numpy.random.permutation(data.index))

k_fold = KFold(n_splits=6)
scores = []
confusion = numpy.array([[0, 0], [0, 0]])
for train_indices, test_indices in k_fold.split(data):
    train_text = data.iloc[train_indices]['text'].values
    train_y = data.iloc[train_indices]['class'].values

    test_text = data.iloc[test_indices]['text'].values
    test_y = data.iloc[test_indices]['class'].values

    pipeline.fit(train_text, train_y)
    predictions = pipeline.predict(test_text)

    confusion += confusion_matrix(test_y, predictions)
    score = f1_score(test_y, predictions, pos_label=FAKE)
    scores.append(score)

print('Total articles classified:', len(data))
print('Score:', sum(scores)/len(scores))
print('Confusion matrix:')
print(confusion)

##count_vectorizer = CountVectorizer(ngram_range=(1, 3), stop_words='english', encoding="utf-8")
##counts = count_vectorizer.fit_transform(data['text'].values)
##
##classifier = MultinomialNB()
##targets = data['class'].values
##classifier.fit(counts, targets)

##UNKNOWNS = [('./data/news/LinksUnknownClass/')]
##
##tests = DataFrame({'text': []})
##for path in UNKNOWNS:
##    tests = tests.append(build_test_frame(path))
##example_counts = count_vectorizer.transform(tests['text'].values)
##predictions = classifier.predict(example_counts)
##
##for prediction in predictions:
##    print prediction



#news=open(file_path_and_name,"r")

#trainingSet=[]
#training with fake news
##path = './data/news/training_fake/'
##for filename in os.listdir(path):
##    file_path_and_name=path+filename
##    news=open(file_path_and_name,"r")
##    read = news.read()
##    trainingSet.append({"text":read,'category': 'fakeNews'})

#training with real news
##path = './data/news/training_real/'    
##for filename in os.listdir(path):
##    file_path_and_name=path+filename
##    news=open(file_path_and_name,"r")
##    read=news.read()
##    trainingSet.append({"text":read ,'category': 'realNews'})
##    
##
##
##
##for news in trainingSet:
##    newsTrainer.train(news['text'], news['category'])


# When you have sufficient trained data, you are almost done and can start to use
# a classifier.

#newsClassifier = Classifier(newsTrainer.data, tokenizer)

# Now you have a classifier which can give a try to classifiy text of news whose
# category is unknown, yet.
##testSet=[]
##path = './data/news/LinksUnknownClass/' 
### for filename in os.listdir(path):
##filename = 'news An Open Letter to My.txt'
##file_path_and_name=path+filename
##news=open(file_path_and_name,"r")
##read=news.read()
##classification = newsClassifier.classify(read)
##print 
##print str(classification) + ' ' + filename

# the classification variable holds the detected categories sorted

