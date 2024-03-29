# -*- coding: utf-8 -*-
"""Travel advisor sentimental analysis

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KbA8IAqh5bmeS9idWr1vCH7kZBCURYxd
"""

import pandas as pd

tweets = pd.read_csv('Airline_tweets.csv', encoding="ISO-8859-1")

tweets.head()

import re
import string
string.punctuation

def removeUrls(text):
  tweetout = re.sub(r'@[a-zA-Z0-9]+','',text)
  re.sub('https?://[a-zA-Z0-9./]+','',tweetout)
  return tweetout

def removeNonAlphaNumericCharac(text):
  text_out = "".join([i for i in text if i not in string.punctuation])
  return text_out

tweets['tweetNoMenUrls'] = tweets['tweet'].apply(lambda x:removeUrls(x))

tweets['tweetNoPuncs'] = tweets['tweetNoMenUrls'].apply(lambda x:removeNonAlphaNumericCharac(x))

def tokenize(text):
  tokens = re.split('\W+', text)
  return tokens

tweets['tokens'] = tweets['tweetNoPuncs'].apply(lambda x:tokenize(x))

import nltk
ps = nltk.PorterStemmer()
def stemming(text):
  out_text=[ps.stem(word) for word in text]
  return out_text

tweets['stemwords'] = tweets['tokens'].apply(lambda x:stemming(x))

import nltk
nltk.download('wordnet')
ps = nltk.WordNetLemmatizer()
def lemmatizeword(text):
  out_text=[ps.lemmatize(word) for word in text]
  return out_text

tweets['lemmawords'] = tweets['tokens'].apply(lambda x:lemmatizeword(x))

tweets.head()

import itertools
stemwords = len(set(list(itertools.chain.from_iterable(tweets['stemwords']))))
lemmawords = len(set(list(itertools.chain.from_iterable(tweets['lemmawords']))))

print(stemwords)
print(lemmawords)

nltk.download('stopwords')

stopwords = nltk.corpus.stopwords.words('english')

def removeStopwords(tokenizedlist):
  text_out = [word for word in tokenizedlist if word not in stopwords]
  return text_out

tweets['seconddataset'] = tweets['stemwords'].apply(lambda x:removeStopwords(x))

#remove low frequencies words

listofuniquewords = itertools.chain.from_iterable(tweets['seconddataset'])

def join_tokens(tokens):
  doc = " ".join([word for word in tokens if not word.isdigit()])
  return doc

tweets['thirddataset'] = tweets['seconddataset'].apply(lambda x:join_tokens(x))

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(listofuniquewords)
countvector = cv.fit_transform(tweets['thirddataset'])
countvectordf = pd.DataFrame(countvector.toarray())
countvectordf.columns = cv.get_feature_names()

countvectordf.head()

#from sklearn.preprocessing import LabelEncoder
#le = LabelEncoder()
#tweets['sentiment'] = le.fit_transform(tweets['sentiment'])
#tweets['sentiment'].value_counts()

from sklearn.model_selection import train_test_split
X = countvectordf
y = tweets['sentiment']

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.20, random_state=0)

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
model = rf.fit(X_train, y_train)

preds = model.predict(X_test)

from sklearn.metrics import classification_report
print((classification_report(y_test, preds)))

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
vectorizer = TfidfVectorizer (max_features=2500, min_df=7, max_df=0.8, stop_words=stopwords.words('english'))
processed_features = vectorizer.fit_transform(tweets['thirddataset']).toarray()

#countvectordf = pd.DataFrame(processed_features)
#countvectordf.columns = processed_features.get_feature_names()

from sklearn.model_selection import train_test_split
X = processed_features
y = tweets['sentiment']

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.20, random_state=0)

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=200, random_state=0)
model = rf.fit(X_train, y_train)

preds = model.predict(X_test)

from sklearn.metrics import classification_report
print((classification_report(y_test, preds)))