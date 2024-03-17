import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
sns.set(style='dark')

#menyiapkan dataframe untuk visualisasi
df = pd.read_csv("clear_bikeshare_day.csv")
df['dteday']=pd.to_datetime(df['dteday'])

st.set_page_config(page_title="Bikesahre Dashboard",
page_icon='line_chart', 
layout='wide')

#membuat fungsi bantu

def create_user_season(df):
    user_season = df.groupby("season").agg({
        "casual" : "sum",
        "registered" : "sum",
        "cnt" : "sum"
    })
    user_season = user_season.reset_index()
    user_season.rename(columns={
        "cnt" : "Total_Riders"
    }, inplace=True) 
    user_season = pd.melt(user_season,
                                      id_vars=['season'],
                                      value_vars=['casual', 'registered'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    user_season['season'] = pd.Categorical(user_season['season'],
                                             categories=['Spring', 'Summer', 'Fall', 'Winter'])
    
    user_season = user_season.sort_values('season')
    
    return user_season

def create_user_month(df):
    user_month=df.resample(rule='ME', on='dteday').agg({
        "casual":"sum",
        "registered":"sum",
        "cnt":"sum"
    })
    user_month.index = user_month.index.strftime('%b-%y')
    user_month = user_month.reset_index()
    user_month.rename(columns={
        "dteday" : "year-month",
        "cnt" : "Total_Riders"
    }, inplace=True)

    return user_month

def create_weekday_users_df(df):
    weekday_users_df = df.groupby("weekday").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    weekday_users_df = weekday_users_df.reset_index()
    weekday_users_df.rename(columns={
        "cnt": "Total_Riders",
    }, inplace=True)
    weekday_users_df = pd.melt(weekday_users_df,
                                      id_vars=['weekday'],
                                      value_vars=['casual', 'registered'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    weekday_users_df['weekday'] = pd.Categorical(weekday_users_df['weekday'],
                                             categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    weekday_users_df = weekday_users_df.sort_values('weekday')
    
    return weekday_users_df

#membuat komponen filtere

min_date = df['dteday'].min()
max_date = df['dteday'].max()

#----sidebar---#

with st.sidebar:
    #st.image("https://w7.pngwing.com/pngs/224/515/png-transparent-edinburgh-bicycle-shop-cycling-logo-bicycle-bicycle-frame-bicycle-logo-thumbnail.png")
    st.header("Visit my Profile:")

    st.markdown("A.A RAFID RAIHAN")

    col1, col2 = st.sidebar.columns(2)

    with col1:
        st.markdown("[![LinkedIn](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](https://www.linkedin.com/in/aa-rafid-raihan/)")

    st.sidebar.header("Filter")

    #untuk tanggal mulai dan akhir dari data input
    start_date, end_date = st.date_input(
        label = 'data filter', min_value = min_date, max_value = max_date, value = [min_date, max_date]
    )

    st.caption('Copyright (c), created by A.A RAFID RAIHAN')

#connect kompenen filter dnegan main_df
main_df = df[
    (df["dteday"] >= str(start_date)) &
    (df["dteday"] <= str(end_date))
]
user_month = create_user_month(main_df)
user_season = create_user_season(main_df)
weekday_users_df = create_weekday_users_df(main_df)

st.title("Bikeshare Dashboard :sparkles:")
st.markdown("##")

col1,col2,col3 = st.columns(3)
with col1:
    total_rider = main_df['cnt'].sum()
    st.metric ("Total riders", value = total_rider)
with col2:
    total_casual = main_df['casual'].sum()
    st.metric ("Total Casual Riders", value = total_casual)
with col3:
    total_rigister = main_df['registered'].sum()
    st.metric("Total Registered Riders", value = total_rigister)

st.markdown("------")

fig = px.line(user_month,
                x='year-month',
                y=['casual','registered', 'Total_Riders'],
                color_discrete_sequence=["skyblue", "orange", "red"],
              markers=True,
              title="Monthly Count of Bikeshare Rides").update_layout (xaxis_title='', 
              yaxis_title='Total Rides')
st.plotly_chart(fig, use_container_width=True)

fig1 = px.bar(weekday_users_df,
              x='weekday',
              y=['count_rides'],
              color='type_of_rides',
              barmode='group',
              color_discrete_sequence=["skyblue", "orange", "red"],
              title='Count of bikeshare rides by weekday').update_layout(xaxis_title='', yaxis_title='Total Rides')


fig2 = px.bar(user_season,
              x='season',
              y=['count_rides'],
              color='type_of_rides',
              color_discrete_sequence=["skyblue", "orange", "red"],
              title='Count of bikeshare rides by season').update_layout(xaxis_title='', yaxis_title='Total Rides')

col4,col5 = st.columns(2)
with col4:
    st.plotly_chart(fig1, use_container_width=True)

with col5:
    st.plotly_chart(fig2, use_container_width=True)


