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



  def post_count(self,df):
    print('\n[INFO]:  Total Post Count ...')
    retweet_count = df['post_retweet_count'].sum()
    post_play_count = df['post_play_count'].sum()
    return len(df),retweet_count,post_play_count
    
  def engaging_people(self,df):
    total_retweets = []
    for name in df['user_title']:
        temp = df[df['user_title']==name]
        total_retweets.append(temp['post_retweet_count'].sum())
    df['total_retweets'] = total_retweets
    df.sort_values(by='total_retweets', ascending=False, inplace=True)
    return df
  
  def key_people(self,df):
    print('\n[INFO]: Extracting Key People ...')
    check = []
    names = []
    handles = []
    n1 = list(dict(df['user_title'].value_counts()).keys())[:6]
    names.extend(n1)
    h1 = list(dict(df['screen_name'].value_counts()).keys())[:6]
    h1 = ['@'+h for h in h1]
    handles.extend(h1)
    
    print('==> Name: ', list(dict(df['user_title'].value_counts()).keys())[0])
    check.append(list(dict(df['user_title'].value_counts()).keys())[0])
    print('==> Twitter: ', list(dict(df['screen_name'].value_counts()).keys())[0])
    print()
        
    df = self.engaging_people(df)

    n3 = list(dict(df['user_title'].value_counts()).keys())[:6]
    names.extend(n3)
    h3 = list(dict(df['screen_name'].value_counts()).keys())[:6]
    h3 = ['@'+h for h in h3]
    handles.extend(h3)
   
    print('==> Name: ', list(df.head(1)['user_title'])[0])
    check.append(list(df.head(1)['user_title'])[0])
    print('==> Twitter: ', list(df.head(1)['screen_name'])[0])
    print()
        
    df.sort_values(by='post_play_count', ascending=False, inplace=True)
        
    n4 = list(dict(df['user_title'].value_counts()).keys())[:6]
    names.extend(n4)
    h4 = list(dict(df['screen_name'].value_counts()).keys())[:6]
    h4 = ['@'+h for h in h4]
    handles.extend(h4)
   
    print('==> Name: ', list(df.head(1)['user_title'])[0])
    print('==> Twitter: ', list(df.head(1)['screen_name'])[0])
        
    print("\n========================================")
    
    return list(set(handles))[:6]
  

  
  
  def originator_name_date(self,df):
    print('\n[INFO]: Extracting Originator & Starting Time/Date ...')
    df['created_at'] = pd.to_datetime(df['created_at'],errors='coerce')
    df['created_at'] = df['created_at'].apply(lambda x: x + datetime.timedelta(hours=5))
    df.sort_values(by='created_at', ascending=False, inplace=True)
    print('\n==> Started By: ', list(df.tail(1)['user_title'])[0], '(@'+list(df.tail(1)['screen_name'])[0]+')')
    print('==> Date & Time Started: ', ' | '.join(str(list(df.tail(1)['created_at'])[0]).split()))
    print("\n========================================")
    return list(df.tail(1)['screen_name'])[0], ' | '.join(str(list(df.tail(1)['created_at'])[0]).split())
  
  def top_location_language(self,df):
    print('\n[INFO]: Extracting Top Location & Language ...')
    
    loc = list(dict(df['user_location'].value_counts()[:1]).keys())[0]
    lang = list(dict(df['post_language'].value_counts()[:1]).keys())[0]
    print('\n==> Top Tweeting Location: ', loc)
    print('==> Top Tweeting Language: ', lang)
    print("\n========================================")
    
    return loc, lang
    
    
  def potential_impressions(self,df):
    print('\n[INFO]: Extracting Potential Impressions ...')
    pi = 0
    df['post_play_count'] = df['post_play_count']. astype('object')
    df['post_play_count'] = pd.to_numeric(df['post_play_count'], errors='coerce')
    handles = df['screen_name'].unique()
    for handle in handles:
      temp = df[df['screen_name']==handle]
      pi += len(temp) * list(temp['post_play_count'])[0]
    return str(pi)


  
   
