import pandas as  pd 
import numpy as np
import string
import os 
import re  
from nltk.corpus import stopwords
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class AntiArmy:
  
  def __init__(self) -> None:
    self.punctuation = list(string.punctuation)
    self.stopwords  = stopwords.words('english') + self.punctuation + ['rt','#bajwa','https','via', 'with', 'new', 'get', 'it', 
                                                                       'well','go',"you",'bring','com','http','yes']
    self.army_keywords = []
    a = open("army.txt", "r")
    for x in a:
      self.army_keywords.append(x.replace("\n", ""))
    
    self.hate_keywords = []
    f = open("hate.txt", "r")
    for x in f:
      self.hate_keywords.append(x.replace("\n", ""))
    

  def remove_numbers(self,text):
    try:
        return re.sub(r'\b\d+(?:\.\d+)?\s+', '', text)
    except:
        return text
    

  def pre_process(self,text):
    
    #remove urls
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    # lowercase
    text=text.lower()
        
    # remove tags
    text=re.sub("</?.*?>"," <> ",text)
        
    # remove speacial characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)

    text= self.remove_numbers(text)
    text= [i for i in text.lower().split() if i not in self.stopwords]
    text = " ".join(text)
    text = text.replace('#', '')
    text= text.replace('@', '')
    text = re.sub((r"^[\W]*"), "", text)
    text = re.sub((r"\s[\W]\s"), ", ", text)
    text = [i for i in text.split() if len(i) > 1]
    text = " ".join(text)
    text = [i for i in text.split() if len(i) < 16]
    text = " ".join(text)
    # text = re.sub(r"[^A-Z/a-z0-9(),!?\'\`.]", " ", text)
    return text
  

  def is_hate(self,x):
    product=0
    x=[i for i in self.hate_keywords if fuzz.token_set_ratio(i,x)>=100]
    y="no"
    if len(x)>=1:
      product=1
      y="yes"
    return y

  def is_army_mention(self,x):
    product=0
    x=[i for i in self.army_keywords if fuzz.token_set_ratio(i,x)>=100]
    y="no"
    if len(x)>=1:
      product=1
      y="yes"
    return y
  
  def filter_data(self,df):
    df['clean_text'] = df['text'].apply(self.pre_process)
    df['is_army_mention'] = df['clean_text'].apply(self.is_army_mention)
#    df = df[df['is_army_mention']=='yes']
    df['is_hate'] = df['clean_text'].apply(self.is_hate)
#    anti_army_df = df[df['is_hate']=='yes']
    return df
