import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import numpy as np
import cufflinks
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from htreport import HashtagReport
import string
from PIL import Image
from arabic_reshaper import arabic_reshaper
from bidi.algorithm import get_display
from nltk.corpus import stopwords
from itertools import islice
from matplotlib import pyplot as plt
#from clean import CleaningText

from army import AntiArmy
army_filters= AntiArmy()


alpha = string.ascii_letters + string.digits

st.set_page_config(page_title="Hashtag Report", page_icon=":bar_chart:", layout="wide")

def main():

  def get_data():

    try:
      directory = os.getcwd()
      csv_files = os.listdir(directory)
      files_ = []
      for item_csv in csv_files:
        if item_csv.endswith(".csv"):
            files_.append(item_csv)
            print("reading file: ",str(files_[0]))
      df = pd.read_csv(str(files_[0]),low_memory=False)
      # Add 'hour' column to dataframe
     
      df["created_at"] = pd.to_datetime(df.created_at)
      df['created_at'] = pd.DatetimeIndex(df.created_at)
      return df
      
                            
    except OSError as error:
      print(error)
      
  def remove_files():
    try:
      directory = os.getcwd()
      csv_files = os.listdir(directory)
      files_ = []
      for item_csv in csv_files:
        if item_csv.endswith(".csv"):
            os.remove(item_csv)
                            
    except OSError as error:
      print(error)
      
  def analyze_hashtags(posts):
        hashtag_dict = {}

        for post in posts:
            for i in post.split():
                if i[0] == '#':
                    current_hashtag = sanitize(i[1:])

                    if len(current_hashtag) > 0:
                        if current_hashtag in hashtag_dict:
                            hashtag_dict[current_hashtag] += 1
                        else:
                            hashtag_dict[current_hashtag] = 1

        return hashtag_dict
        
  def analyze_screen_name(posts):
        hashtag_dict = {}

        for post in posts:
            for i in post.split():
                if i[0] == '@':
                    current_hashtag = sanitize(i[1:])

                    if len(current_hashtag) > 0:
                        if current_hashtag in hashtag_dict:
                            hashtag_dict[current_hashtag] += 1
                        else:
                            hashtag_dict[current_hashtag] = 1

        return hashtag_dict
        
  def sanitize(s):
    s2 = ''
    for i in s:
        if i in alpha:
            s2 += i
        else:
            break
    return s2


  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/


  ht_report=HashtagReport()


  df = get_data()
  print(df)
  df = df[:3000]
  army_df = df.copy()
  army_df = army_filters.filter_data(army_df)
  hate_len = army_df[army_df['is_hate']=='yes']
  anti_army_len = hate_len[hate_len['is_army_mention']=='yes']
  # ---- MAINPAGE ----
  st.title(":bar_chart: Twitter Hashtag Report")
  mystyle = '''
      <style>
          p {
              text-align: justify;
          }
      </style>
      '''
  st.markdown(mystyle, unsafe_allow_html=True)
  
  hashtags_title = df[["hashtags"]]
  hashtags_title = hashtags_title.groupby(['hashtags']).size().to_frame().sort_values([0], ascending = False).head(1).reset_index()
  hashtags_title.columns = ['hashtags', 'count']
  print("hashtag tile",)
  hashtag_name = str(hashtags_title['hashtags'].iloc[0])
  hashtag_name = "#"+hashtag_name
#  hashtag_name = "BajwaTraitor"
#  st.markdown("<h1 style='text-align: center; color: Blue;'></h1>", unsafe_allow_html=True)
  st.markdown(f'<h2 style="text-align: center;font-size:30px;color:#1A4164">{hashtag_name}</h2>', unsafe_allow_html=True)
   


  original_tweet_count_, retweet_count_, total_tweet_count_,unique_users = ht_report.original_tweet_count(df)
  df = ht_report.engaging_people(df)
  key_people = ht_report.key_people(df)
  start_name, start_date_=ht_report.originator_name_date(df)
  location, lang=ht_report.top_location_language(df)
  impressions=ht_report.potential_impressions(df)

  # TOP KPI's

  left_column, middle_column,middle_column2,right_column = st.columns(4)
  with left_column:
      st.markdown(f'<h1 style="text-align:center;color:#1F4E79;font-size:30px;">{"Total Tweets"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{total_tweet_count_}</h2>', unsafe_allow_html=True)

  with middle_column:
      st.markdown(f'<h1 style="text-align:center;color:#1F4E79;font-size:30px;">{"HateSpeech Tweets"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{str(len(hate_len))}</h2>', unsafe_allow_html=True)
      
  with middle_column2:
      st.markdown(f'<h1 style="text-align:center;color:#1F4E79;font-size:30px;">{"Anti-Army Tweets"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{str(len(anti_army_len))}</h2>', unsafe_allow_html=True)
        
  with right_column:
      st.markdown(f'<h1 style="text-align:center;color:#1F4E79;font-size:30px;">{"Impressions"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{impressions}</h2>', unsafe_allow_html=True)

  left_column_r3, middle_column_r3,middle_column2_r3,right_column_r3 = st.columns(4)
  with left_column_r3:
      st.header("")

  with middle_column_r3:
      st.header(" ")
  with middle_column2_r3:
      st.header(" ")
  with right_column_r3:
      st.header(" ")
  

  left_column_r2, middle_column_r1,middle_column2_r1,right_column_r1 = st.columns(4)
  with left_column_r2:
      st.markdown(f'<h1 style="text-align:center;color:#1F4E79;font-size:30px;">{"Startedby"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:18px;">{start_name}</h2>', unsafe_allow_html=True)
  with middle_column_r1:
      st.markdown(f'<h1 style="text-align:center;color:#1F4E79;font-size:30px;">{"Started On"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:18px;">{start_date_}</h2>', unsafe_allow_html=True)
  with middle_column2_r1:
      st.markdown(f'<h1 style="text-align:center;color:#1F4E79;font-size:30px;">{"Location"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{location}</h2>', unsafe_allow_html=True)
  with right_column_r1:
      st.markdown(f'<h1 style="text-align:center;color:#1F4E79;font-size:30px;">{"Unique Users Count"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{unique_users}</h2>', unsafe_allow_html=True)

  st.markdown("""---""")

  def original_tweet(is_retweet):
    if is_retweet==1:
      return 0
    else:
      return 1

  def retweet_tweet(is_retweet):
    if is_retweet==1:
      return 1
    else:
      return 0
      


  df['retweeted'] = df['is_retweet'].apply(retweet_tweet)
  df['original_tweet'] = df['is_retweet'].apply(original_tweet)
  filter_data = df[['created_at','original_tweet','retweeted']]
  daily_cases = filter_data.groupby(pd.Grouper(key="created_at", freq="T")).sum().reset_index()
  #line_column = st.columns(1)

  fig = daily_cases.iplot(kind="line",asFigure=True,
                              x="created_at", y=["original_tweet","retweeted"],title="<b>Tweet Trajectory </b>")


  st.plotly_chart(fig,use_container_width=True)

  
  hashtags_list = df['text'].to_list()
  hashtags_count = analyze_hashtags(hashtags_list)
  hashtags_df = pd.DataFrame(hashtags_count.items(),columns=['hashtags', 'count'])
  hashtags_df = hashtags_df.sort_values('count',ascending=False)
  
  
   
  screen_list = df['text'].to_list()
  screen_names_count = analyze_screen_name(screen_list)
  screen_df = pd.DataFrame(screen_names_count.items(),columns=['mentions_screen_name', 'count'])
  screen_df = screen_df.sort_values('count',ascending=False)
  
  
  army_df['HateSpeech'] =   army_df['is_hate'].apply({'yes':'HateSpeech','no':'Normal-Speech'}.get)
  anti_army_df = army_df.copy()
  army_df = army_df[['HateSpeech']]
  
  army_df=army_df[['HateSpeech']].value_counts().reset_index(name='count')
  fig_army = px.bar(army_df, x ='HateSpeech', y = 'count',color="HateSpeech",
                     color_discrete_sequence = ["green", "red",])
                     
  fig_army.update_yaxes(showgrid=False)
  fig_army.update_xaxes(categoryorder='total descending')
  fig_army.update_traces(hovertemplate=None)
  fig_army.update_layout(margin=dict(t=70, b=0, l=70, r=40),
                        hovermode="x unified",
                        xaxis_tickangle=360,
                        xaxis_title=' ', yaxis_title=" ",
                        plot_bgcolor='#e9eef0', paper_bgcolor='#e9eef0',
                        title_font=dict(size=25, color='#04080a', family="Lato, sans-serif"),
                        font=dict(color='#04080a'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                          )
  fig_army_pie = px.pie(army_df,
                      values="count",
                      names="HateSpeech",
                      title="<b>HateSpeech Vs Normal </b>",
                      hole=.3)
  fig_army_pie.update_layout(legend=dict(
      yanchor="top",
      y=0.99,
      xanchor="left",
      x=0.01
  ))

  fig_army_pie.update_traces(marker=dict(colors=['#339970','#80302b']))

  fig_army_pie.update_yaxes(tickfont_family="Arial Black")
  
  anti_df = army_df.copy()
  anti_df = anti_army_df[anti_army_df['HateSpeech']=='HateSpeech']

  anti_df = anti_df[['is_army_mention']]
  anti_df['is_army_mention'] =   anti_df['is_army_mention'].apply({'yes':'Anti-Army','no':'HateSpeech'}.get)
  anti_df = anti_df[['is_army_mention']].value_counts().reset_index(name='count')


  fig_anti_army = px.pie(anti_df,
                      values="count",
                      names="is_army_mention",
                      title="<b>HateSpeech Vs Anti-Army </b>",
                      hole=.3)
  fig_anti_army.update_layout(legend=dict(
      yanchor="top",
      y=0.99,
      xanchor="left",
      x=0.01
  ))

  fig_anti_army.update_traces(marker=dict(colors=['#339970','#80302b']))

  left_army, right_army = st.columns(2)

  with right_army:
    st.plotly_chart(fig_army_pie, use_container_width=True)
  with left_army:
    st.plotly_chart(fig_anti_army, use_container_width=True)
  
  

#  hashtags_graph_data = (
#        hashtags_df.groupby(by=["hashtags"]).sum()[["count"]].sort_values(by="count")
#  )
##  sales_by_product_line = sales_by_product_line.sort_values('count',ascending=False)
#  hashtags_graph_data = hashtags_graph_data.tail()
#  fig_product_sales = px.bar(
#      hashtags_graph_data,
#      x="count",
#      y=hashtags_graph_data.index,
#      orientation="h",
#
#      title="<b>Top Associated Hashtags</b>",
#      color_discrete_sequence=["#008080"] * len(hashtags_graph_data),
#      template="plotly_white",
#  )
#  fig_product_sales.update_layout(
#      plot_bgcolor="rgba(0,0,0,0)",
#      xaxis=(dict(showgrid=False))
#  )
#  fig_product_sales.update_layout(
#    title="<b>Top Associated Hashtags</b>",
#    xaxis_title="Count",
#    yaxis_title="hashtags",
#    font=dict(
#        family="Courier New, monospace",
#        size=12,
#        color="Black"
#        )
#    )
#
#  fig_product_sales.update_yaxes(tickfont_family="Arial Black")
#  df['retweet_count'] = df['retweet_count'].apply(int)
#  df_screen = df[["screen_name","retweet_count"]]
#  retweet_by_screen_name = (
#      df_screen.groupby(by=["screen_name"]).sum()[["retweet_count"]].sort_values(by="retweet_count")
#  )
##  print("Retweeted count",retweet_by_screen_name.tail())
#  retweet_by_screen_name = retweet_by_screen_name.tail()
#  fig_screen_names = px.bar(
#      retweet_by_screen_name,
#      x="retweet_count",
#      y=retweet_by_screen_name.index,
#      orientation="h",
#
#      title="<b>Most retweeted User </b>",
#
#      color_discrete_sequence=["#336699"] * len(retweet_by_screen_name),
#      template="plotly_dark",
#  )
#
#  fig_screen_names.update_layout(
#      plot_bgcolor="rgba(0,0,0,0)",
#      xaxis=(dict(showgrid=False))
#  )
#
#  fig_screen_names.update_layout(
#    title="<b>Most retweeted User </b>",
#    xaxis_title="Count",
#    yaxis_title="retweeted",
#    font=dict(
#        family="Courier New, monospace",
#        size=12,
#        color="Black"
#        )
#    )
#  fig_screen_names.update_yaxes(tickfont_family="Arial Black")
#
#  left_column, right_column = st.columns(2)
#  left_column.plotly_chart(fig_screen_names, use_container_width=True)
#  right_column.plotly_chart(fig_product_sales, use_container_width=True)
#
#  df_screen = df[["screen_name","original_tweet"]]
#  tweet_by_screen_name = (
#      df_screen.groupby(by=["screen_name"]).sum()[["original_tweet"]].sort_values(by="original_tweet")
#  )
#
#
#  tweet_by_screen_name = tweet_by_screen_name.tail()
#  fig_screen_names_tweets = px.bar(
#      tweet_by_screen_name,
#      x="original_tweet",
#      y=tweet_by_screen_name.index,
#      orientation="h",
#      title="<b>Most Original tweets by User </b>",
#      color_discrete_sequence=["#993366"] * len(tweet_by_screen_name),
#      template="plotly_dark",
#  )
#  fig_screen_names_tweets.update_layout(
#      plot_bgcolor="rgba(0,0,0,0)",
#      xaxis=(dict(showgrid=False))
#  )
#
#  fig_screen_names_tweets.update_layout(
#    title="<b>Most Original tweets by User </b>",
#    xaxis_title="Count",
#    yaxis_title="original_tweet",
#    font=dict(
#        family="Courier New, monospace",
#        size=12,
#        color="Black"
#        )
#    )
#  fig_screen_names_tweets.update_yaxes(tickfont_family="Arial Black")
#
#  df_source = df[["source"]]
#  df_source = df_source.groupby(['source']).size().to_frame().sort_values([0], ascending = False).head(5).reset_index()
#  df_source.columns = ['source', 'count']
#
#  fig_source = px.pie(df_source,
#                      values="count",
#                      names="source",
#                      title="<b>Source </b>",
#                      hole=.3,
#
#                      )
#
#  fig_source.update_yaxes(tickfont_family="Arial Black")
#
#  fig_source.update_traces(marker=dict(colors=['#993366', '#009999','#990033','#006699','#339970']))
#
#  left_column2, right_column2 = st.columns(2)
#  left_column2.plotly_chart(fig_screen_names_tweets, use_container_width=True)
#  right_column2.plotly_chart(fig_source, use_container_width=True)
#
#  df_lang = df[["lang"]]
#  df_lang = df_lang[df_lang['lang']!='und']
#  df_lang = df_lang.groupby(['lang']).size().to_frame().sort_values([0], ascending = False).head(5).reset_index()
#  df_lang.columns = ['lang', 'count']
#
#  fig_lang = px.pie(df_lang,
#                      values="count",
#                      names="lang",
#                      title="<b>Language Used </b>",
#                      hole=.3)
#  fig_lang.update_layout(legend=dict(
#      yanchor="top",
#      y=0.99,
#      xanchor="left",
#      x=0.01
#  ))
#
#  fig_lang.update_traces(marker=dict(colors=['#006699','#339970','#AEAEAE','#FFC000', '#993366', '#009999','#990033',]))
#
#  fig_lang.update_yaxes(tickfont_family="Arial Black")
#
#  screen_name_mentioed = (
#            screen_df.groupby(by=["mentions_screen_name"]).sum()[["count"]].sort_values(by="count")
#  )
#  screen_name_mentioed = screen_name_mentioed.tail()
#  fig_screen_name_mentioned = px.bar(
#      screen_name_mentioed,
#      x="count",
#      y=screen_name_mentioed.index,
#      orientation="h",
#
#      title="<b>Most Mentioned Screen Names </b>",
#      color_discrete_sequence=["#FF9933"] * len(screen_name_mentioed),
#      template="plotly_white",
#  )
#  fig_screen_name_mentioned.update_layout(
#      plot_bgcolor="rgba(0,0,0,0)",
#      xaxis=(dict(showgrid=False))
#  )
#
#  fig_screen_name_mentioned.update_layout(
#    title="<b>Most Mentioned Screen Names </b>",
#    xaxis_title="Count",
#    yaxis_title="mentioned_screen_names",
#    font=dict(
#        family="Courier New, monospace",
#        size=12,
#        color="Black"
#        )
#    )
#  fig_screen_name_mentioned.update_yaxes(tickfont_family="Arial Black")
#
#  left_column3, right_column3 = st.columns(2)
#  left_column3.plotly_chart(fig_lang, use_container_width=True)
#  right_column3.plotly_chart(fig_screen_name_mentioned, use_container_width=True)
#
#  location_data = df[['location']]
#  location_data = location_data.dropna()
#
#  def get_cities(list_1):
#
#    list_1 = list_1.split(",")
#    if len(list_1)==1:
#      return list_1[0]
#    elif len(list_1)>1:
#      return list_1[0]
#    else:
#      return ""
#
#  def get_country(list_1):
#    list_1 = list_1.split(",")
#    if len(list_1)>1:
#      return list_1[1]
#    else:
#      return ""
#
#  location_data['cities'] = location_data['location'].apply(get_cities)
#  location_data['country'] = location_data['location'].apply(get_country)
#
#  cities = location_data.groupby(['cities']).size().to_frame().sort_values([0], ascending = False).head(5).reset_index()
#  cities.columns = ['cities', 'count']
#
#  cities_mentioned = (
#          cities.groupby(by=["cities"]).sum()[["count"]].sort_values(by="count")
#  )
#  fig_cities_mentioned = px.bar(
#      cities_mentioned,
#      x="count",
#      y=cities_mentioned.index,
#      orientation="h",
#
#      title="<b>Most Frequent Cities mentioned </b>",
#      color_discrete_sequence=["#008080"] * len(cities_mentioned),
#      template="plotly_white",
#  )
#  fig_cities_mentioned.update_layout(
#      plot_bgcolor="rgba(0,0,0,0)",
#      xaxis=(dict(showgrid=False))
#  )
#
#  fig_cities_mentioned.update_layout(
#    title="<b>Most Frequent Locations mentioned </b>",
#    xaxis_title="Count",
#    yaxis_title="Location",
#    font=dict(
#        family="Courier New, monospace",
#        size=13,
#        color="Black"
#        )
#    )
#  fig_cities_mentioned.update_yaxes(tickfont_family="Arial Black")
#
#  df = df.dropna(subset=['hashtags'])
#
##  df['text'] = df['text'].apply(text_clean.clean_text)
#  hashtags_title1 = hashtags_df[["hashtags"]].values
#  hashtags_title1 = str(hashtags_title1)
#
#  stop_ar = stopwords.words('english')
#  # add more stop words here like numbers, special characters, etc. It should be customized for your project
#
#  top_words = {}
#  words = hashtags_title1.split()
#
#  for w in words:
#    if w in stop_ar:
#        continue
#    else:
#        if w not in top_words:
#            top_words[w] = 1
#        else:
#            top_words[w] +=1
#
#  top_words = {k: v for k, v in sorted(top_words.items(), key=lambda item: item[1], reverse = True)}
#
#  def take(n,iterable):
#    "Return first n time of the iterable as a list"
#    return list(islice(iterable,n))
#
#  wc = take(150, top_words.items())
#
#  dic_data = {}
#
#  for t in wc:
#    print(t[0])
#    print(type(t[0]))
#    x = t[0].replace("['", '')
#    x = x.replace("[", '')
#    x = x.replace("']", '')
#    r = arabic_reshaper.reshape(x) # connect Arabic letters
#    bdt = get_display(r) # right to left
#    dic_data[bdt] = t[1]
#
#  # Plot
#  wc = WordCloud(background_color="white", width=1600, height=800,max_words=200, font_path='Zeytoon Bold.ttf').generate_from_frequencies(dic_data)
#  plt.figure(figsize=(16,8))
#  plt.imshow(wc, interpolation='bilinear')
#  plt.axis("off")
#
#
#  left_column4, right_column4 = st.columns(2)
#  left_column4.plotly_chart(fig_cities_mentioned, use_container_width=True)
#  right_column4.pyplot(plt)
#
#  # ---- HIDE STREAMLIT STYLE ----
#  hide_st_style = """
#              <style>
#              #MainMenu {visibility: hidden;}
#              footer {visibility: hidden;}
#              header {visibility: hidden;}
#              </style>
#              """
  #st.markdown(hide_st_style, unsafe_allow_html=True)
  remove_files()
  
 
st.sidebar.header("Please Filter Here:")
uploaded_file = st.sidebar.file_uploader("Upload CSV file",type=["csv"])
button = st.sidebar.button("Generate Hashtags")
try:
    if uploaded_file:
        with open(os.path.join(uploaded_file.name),"wb") as f:
            f.write(uploaded_file.getbuffer())
            st.sidebar.success("Uploaded Successfully.....")
    
except Exception as e:
    print(e)
    pass
try:
    if button:
        main()
        
except Exception as e:
    st.write("Please upload file using Side bar",e)



