import pandas as pd
import csv
import datetime
import jinja2
import re
import os

class HashtagReport:

  def __init__(self):

    self.font = {'family': 'serif',
        'color':  '#3883ab',
        'weight': 'bold',
        'size': 12,
         }



  def original_tweet_count(self,df):
    print('\n[INFO]: Original Tweet Count ...')
    
    df['retweets'] = pd.to_numeric(df['is_retweet'], errors='coerce')
    original_tweet_count = df[df['is_retweet']==0]
    original_tweet_count = len(original_tweet_count)
    print('==> Original Tweet Count: ', original_tweet_count)
 
    retweet_count = df[df['is_retweet']==1]
    retweet_count = len(retweet_count)
    print('==> Retweet Count: ', retweet_count)
    
    print('==> Total Tweet Count: ', len(df))
    print("\n========================================")
    return original_tweet_count, retweet_count, len(df), df['screen_name'].nunique()
  
  def engaging_people(self,df):
  
    total_retweets = []
    for name in df['name']:
        temp = df[df['name']==name]
        total_retweets.append(temp['is_retweet'].sum())
    df['total_retweets'] = total_retweets
    df['total_retweets'] = df['total_retweets'].apply(int)
    df.sort_values(by='total_retweets', ascending=False, inplace=True)
    return df

  def key_people(self,df):
    print('\n[INFO]: Extracting Key People ...')
    check = []
    names = []
    handles = []
    n1 = list(dict(df['name'].value_counts()).keys())[:6]
    names.extend(n1)
    h1 = list(dict(df['screen_name'].value_counts()).keys())[:6]
    h1 = ['@'+h for h in h1]
    handles.extend(h1)
    
    print('==> Name: ', list(dict(df['name'].value_counts()).keys())[0])
    check.append(list(dict(df['name'].value_counts()).keys())[0])
    print('==> Twitter: ', list(dict(df['screen_name'].value_counts()).keys())[0])
    print()
        
    df = self.engaging_people(df)

    n3 = list(dict(df['name'].value_counts()).keys())[:6]
    names.extend(n3)
    h3 = list(dict(df['screen_name'].value_counts()).keys())[:6]
    h3 = ['@'+h for h in h3]
    handles.extend(h3)
   
    print('==> Name: ', list(df.head(1)['name'])[0])
    check.append(list(df.head(1)['name'])[0])
    print('==> Twitter: ', list(df.head(1)['screen_name'])[0])
    print()
        
    df.sort_values(by='followers_count', ascending=False, inplace=True)
        
    n4 = list(dict(df['name'].value_counts()).keys())[:6]
    names.extend(n4)
    h4 = list(dict(df['screen_name'].value_counts()).keys())[:6]
    h4 = ['@'+h for h in h4]
    handles.extend(h4)
   
    print('==> Name: ', list(df.head(1)['name'])[0])
    print('==> Twitter: ', list(df.head(1)['screen_name'])[0])
        
    print("\n========================================")
    
    return list(set(handles))[:6]
  
  def originator_name_date(self,df):
    print('\n[INFO]: Extracting Originator & Starting Time/Date ...')
    df['created_at'] = pd.to_datetime(df['created_at'],errors='coerce')
    df['created_at'] = df['created_at'].apply(lambda x: x + datetime.timedelta(hours=5))
    df.sort_values(by='created_at', ascending=False, inplace=True)
    print('\n==> Started By: ', list(df.tail(1)['name'])[0], '(@'+list(df.tail(1)['screen_name'])[0]+')')
    print('==> Date & Time Started: ', ' | '.join(str(list(df.tail(1)['created_at'])[0]).split()))
    print("\n========================================")
    return '@'+list(df.tail(1)['screen_name'])[0], ' | '.join(str(list(df.tail(1)['created_at'])[0]).split())
  
  def top_location_language(self,df):
    print('\n[INFO]: Extracting Top Location & Language ...')
    try:
        loc = list(dict(df['location'].value_counts()[:1]).keys())[0]
    except:
        loc =""
    try:
        lang = list(dict(df['lang'].value_counts()[:1]).keys())[0]
    except:
        lang=""
    print('\n==> Top Tweeting Location: ', loc)
    # try:
    #     lang = language(df['lang'].value_counts()[:1].index.tolist()[0])['Name']
    # except:
    #     lang = language(df['lang'].value_counts()[:2].index.tolist()[1])['Name']
    print('==> Top Tweeting Language: ', lang)
    print("\n========================================")
    
    return loc, lang
  
  def potential_impressions(self,df):
    print('\n[INFO]: Extracting Potential Impressions ...')
    pi = 0
    df['followers_count'] = df['followers_count']. astype('object')
    df['followers_count'] = pd.to_numeric(df['followers_count'], errors='coerce')
    handles = df['screen_name'].unique()
    for handle in handles:
      temp = df[df['screen_name']==handle]
      pi += len(temp) * list(temp['followers_count'])[0]
    return str(pi)


  
   
