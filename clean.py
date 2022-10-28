
import pandas as pd
import numpy as np

import string
import os
import re
# import preprocessor as p
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import sent_tokenize, word_tokenize, pos_tag
lemma = WordNetLemmatizer()
# from langdetect import detect_langs
import emoji
lemma = WordNetLemmatizer()
punctuation = list(string.punctuation)


class CleaningText:

    def __init__(self):
        
        self.punctuation = list(string.punctuation)
        self.stop  = stopwords.words('english') + self.punctuation + ['[',"['","']",'\n','/n','rt','میں','via', 'with', 'new', 'get', 'it', 'go',"you"]

        path = 'stopwords-ur.txt'
        self.urdu_stop_words = pd.read_csv(path, header=None)
        self.urdu_stop_words = self.urdu_stop_words[0].unique().tolist()
 
        self.stop = self.stop + self.urdu_stop_words  
      
        self.table = str.maketrans({key: None for key in string.punctuation})
        
    def clean_function(self, x):

        x = emoji.demojize(x)
        # x=p.clean(x)
        return x

    def remove_twitter_handles(self, text):

        try:
            text = re.sub('@[^\s]+', '', text)
        except:
            pass
        return text

    def remove_numbers(self, text):

        try:
            return re.sub(r'\b\d+(?:\.\d+)?\s+', '', text)
        except:
            return text

    def clean_text(self, x):
        x = emoji.demojize(x)
        # x = p.clean(x)
        x = self.remove_twitter_handles(x)
        x = self.remove_numbers(x)
        x = x.replace('#', '')
        x = x.replace('@', '')
        x = x.replace("['", '')
        x = x.replace("']", '')
        x = [i for i in x.lower().split() if i not in self.stop]
        x = " ".join(x)
#         x = re.sub(r"[^A-Z/a-z0-9(),!?\'\`.]", " ", x)
        x = re.sub((r"^[\W]*"), "", x)
        x = re.sub((r"\s[\W]\s"), ", ", x)
        x = [i for i in x.split() if len(i) > 1]
        x = " ".join(x)
        x = [i for i in x.split() if len(i) < 16]
        x = " ".join(x)
       
        return x
