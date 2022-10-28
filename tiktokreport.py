


import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import numpy as np
import cufflinks
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string
alpha = string.ascii_letters + string.digits
from tiktok import HashtagReport

st.set_page_config(page_title="Tiktok Hashtag Report", page_icon=":bar_chart:", layout="wide")

def tiktok_main():

      
  st.set_page_config(page_title="Tiktok Hashtag Report", page_icon=":bar_chart:", layout="wide")
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
        
  def sanitize(s):
    s2 = ''
    for i in s:
        if i in alpha:
            s2 += i
        else:
            break
    return s2

  def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/


  ht_report=HashtagReport()


  ## ---- SIDEBAR ----

#  city = st.sidebar.multiselect(
#      "Select the City:",
#      options=df["name"].unique(),
#      default=df["name"].unique()
#  )
  #


  # ---- MAINPAGE ----
  st.title(":bar_chart: Tiktok Hashtag Report")
  mystyle = '''
      <style>
          p {
              text-align: justify;
          }
      </style>
      '''
  st.markdown(mystyle, unsafe_allow_html=True)
  
  hashtags_list = df['post_hashtags'].to_list()
  hashtags_count = analyze_hashtags(hashtags_list)
  hashtags_df = pd.DataFrame(hashtags_count.items(),columns=['hashtags', 'count'])
  hashtags_df = hashtags_df.sort_values('count',ascending=False)

  
  hashtags_df = hashtags_df[hashtags_df['hashtags']!='foryou']
  print(hashtags_df)
  hashtag_name = str(hashtags_df['hashtags'].iloc[0])

  hashtag_name = "#"+hashtag_name
  st.markdown(f'<h2 style="text-align: center;font-size:30px;color:#1A4164">{hashtag_name}</h2>', unsafe_allow_html=True)
 
  total_post_count_,retweet_count,post_play_count=ht_report.post_count(df)
  post_play_count = human_format(int(post_play_count))
  df = ht_report.engaging_people(df)
  key_people = ht_report.key_people(df)
  start_name, start_date_=ht_report.originator_name_date(df)
  location, lang=ht_report.top_location_language(df)
  impressions=ht_report.potential_impressions(df)
  impressions = human_format(int(impressions))
  # TOP KPI's

  left_column, middle_column,middle_column2,right_column = st.columns(4)
  with left_column:
      st.markdown(f'<h1 style="text-align:center;color:##1F4E79;font-size:30px;">{"Total Post Count"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{total_post_count_}</h2>', unsafe_allow_html=True)

  with middle_column:
      st.markdown(f'<h1 style="text-align:center;color:##1F4E79;font-size:30px;">{"Retweet Count"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{retweet_count}</h2>', unsafe_allow_html=True)
      
  with middle_column2:
      st.markdown(f'<h1 style="text-align:center;color:##1F4E79;font-size:30px;">{"Impressions"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{impressions}</h2>', unsafe_allow_html=True)
  with right_column:
      st.markdown(f'<h1 style="text-align:center;color:##1F4E79;font-size:30px;">{"Play count"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{post_play_count}</h2>', unsafe_allow_html=True)

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
      st.markdown(f'<h1 style="text-align:center;color:##1F4E79;font-size:30px;">{"Startedby"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:18px;">{start_name}</h2>', unsafe_allow_html=True)
  with middle_column_r1:
      st.markdown(f'<h1 style="text-align:center;color:##1F4E79;font-size:30px;">{"Started On"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:18px;">{start_date_}</h2>', unsafe_allow_html=True)
  with middle_column2_r1:
      st.markdown(f'<h1 style="text-align:center;color:##1F4E79;font-size:30px;">{"Location"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{location}</h2>', unsafe_allow_html=True)
  with right_column_r1:
      st.markdown(f'<h1 style="text-align:center;color:##1F4E79;font-size:30px;">{"Language"}</h1>', unsafe_allow_html=True)
      st.markdown(f'<h2 style="text-align: center;font-size:24px;">{lang}</h2>', unsafe_allow_html=True)

  st.markdown("""---""")

  filter_data = df[['post_created_time','post_play_count']]
  daily_cases = filter_data.groupby(pd.Grouper(key="post_created_time", freq="D")).sum().reset_index()

  fig = daily_cases.iplot(kind="line",asFigure=True,
                                  x="post_created_time", y=['post_play_count'],title="<b>Hashtag Reach Count per Day </b>")
  st.plotly_chart(fig,use_container_width=True)
#
#
  hashtags_data = df[["screen_name"]]
  hashtags_data = hashtags_data.groupby(['screen_name']).size().to_frame().sort_values([0], ascending = False).head(5).reset_index()
  hashtags_data.columns = ['screen_name', 'count']

  # SALES BY PRODUCT LINE [BAR CHART]
  sales_by_screen_name = (
      hashtags_data.groupby(by=["screen_name"]).sum()[["count"]].sort_values(by="count")
  )
  fig__screen_names = px.bar(
      sales_by_screen_name,
      x="count",
      y=sales_by_screen_name.index,
      orientation="h",
      
      title="<b>Videos Posted by..</b>",
      color_discrete_sequence=["#05b7ff"] * len(sales_by_screen_name),
      template="plotly_dark",)
      
  fig__screen_names.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      xaxis=(dict(showgrid=False))
  )
 
  fig__screen_names.update_layout(
    title="<b>Videos Posted by</b>",
    xaxis_title="Count",
    yaxis_title="Screen Name",
    font=dict(
        family="Courier New, monospace",
        size=12,
        color="Black"
        )
    )
      
      
  df_source = df[["post_language"]]
  df_source = df_source.groupby(['post_language']).size().to_frame().sort_values([0], ascending = False).head(5).reset_index()
  df_source.columns = ['post_language', 'count']

  fig_source = px.pie(df_source,
                          values="count",
                          names="post_language",
                          title="<b>Language Used</b>",
                          hole=.3,)
                          
  fig_source.update_yaxes(tickfont_family="Arial Black")
  fig_source.update_traces(marker=dict(colors=['#339970','#993366', '#009999','#990033','#006699']))
                          
  fig_source.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      xaxis=(dict(showgrid=False))
  )
    

  df_location = df[["user_location"]]
  df_location = df_location.groupby(['user_location']).size().to_frame().sort_values([0], ascending = False).head(5).reset_index()
  df_location.columns = ['user_location', 'count']

  fig_location = px.pie(df_location,
                          values="count",
                          names="user_location",
                          title="<b>User Location  </b>",
                          hole=.3,)

  fig_location.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      xaxis=(dict(showgrid=False))
      )
      
  fig_location.update_layout(legend=dict(
      yanchor="top",
      y=0.99,
      xanchor="left",
      x=0.01
  ))
  fig_location.update_yaxes(tickfont_family="Arial Black")
  fig_location.update_traces(marker=dict(colors=['#339970','#993366', '#009999','#990033','#006699']))
  
  hashtags_df = (
          hashtags_df.groupby(by=["hashtags"]).sum()[["count"]].sort_values(by="count"))

  hashtags_df = hashtags_df.tail()
  fig_hashtag = px.bar(
      hashtags_df,
      x="count",
      y=hashtags_df.index,
      orientation="h",
      
      title="<b>Top Associated Hashtags</b>",
      color_discrete_sequence=["#008080"] * len(hashtags_df),
      template="plotly_white",
  )
  fig_hashtag.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      xaxis=(dict(showgrid=False))
  )
  fig_hashtag.update_layout(
    title="<b>Top Associated Hashtags</b>",
    xaxis_title="Count",
    yaxis_title="hashtags",
    font=dict(
        family="Courier New, monospace",
        size=12,
        color="Black"
        )
    )
      
  

  left_column, right_column = st.columns(2)
  left_column.plotly_chart(fig_hashtag, use_container_width=True)
  right_column.plotly_chart(fig__screen_names, use_container_width=True)

  left_column2, right_column2 = st.columns(2)
  left_column2.plotly_chart(fig_location, use_container_width=True)
  right_column2.plotly_chart(fig_source, use_container_width=True)
  
