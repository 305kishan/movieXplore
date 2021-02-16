import streamlit as st
import pandas as pd
pd.set_option('display.max_colwidth', -1)

import urllib.request, urllib.parse, urllib.error
import json
import requests

import matplotlib.pyplot as plt
plt.style.use("ggplot")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


page_bg_img = '''
<style>
body {
background-image: url("https://www.wallpapertip.com/wmimgs/167-1677732_4k-a-simple-gradient-19201080-free-download-background.jpg");
background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)


def urlGenerator(title):
    serviceUrl = 'http://www.omdbapi.com/?'
    apiKey='&apikey=7180e7d8'
    url = serviceUrl + urllib.parse.urlencode({'t':title}) + apiKey
    inputInfo = urllib.request.urlopen(url)
    return inputInfo
    

def movieDataGenerator(inputInfo):
    data = inputInfo.read()
    json_data = json.loads(data)
    movieDf = pd.DataFrame(json_data)
    rating = json_data['Ratings']
    ratingDf = pd.DataFrame(rating)
    return movieDf,ratingDf


def seriesDataGenerator(inputInfo):
    data = inputInfo.read()
    json_data = json.loads(data)
    seriesDf = pd.DataFrame(json_data)
    rating = json_data['Ratings']
    ratingDf = pd.DataFrame(rating)
    return seriesDf,ratingDf
    


def movieInput():
    title = st.text_input("Enter movie Name",'Titanic')
    inputInfo = urlGenerator(title)
    if st.button("SUBMIT"):
        try:
            movieDf,ratingDf = movieDataGenerator(inputInfo)
            return movieDf, ratingDf
        except:
            st.text("This input currently Can't be processed, try some other movies")
            

 
def seriesInput():
    title = st.text_input("Enter A Series Name","The Office")
    inputInfo = urlGenerator(title)
    if st.button("SUBMIT"):
        try:
            seriesDf,ratingDf = seriesDataGenerator(inputInfo)
            return seriesDf, ratingDf
        except:
            st.text("This input currently Can't be processed, try some other movies")

def twoMovieinput():
    st.text("Enter Two Movies for Comparision")
    d = []
    c = st.text_input("Enter First Movie ", "Titanic")
    b = st.text_input("Enter Second Movie ", "3 Idiots")
    d.append(c)
    d.append(b)
    if st.button("Compare"):
        e = d
        return e
    
def twoSeriesinput():
    st.text("Enter Two Series for Comparision")
    d = []
    c = st.text_input("Enter First Series ", "The Office")
    b = st.text_input("Enter Second Series ", "Friends")
    d.append(c)
    d.append(b)
    if st.button("Compare"):
        e = d
        return e


def movieAnalysis():
    try:
        movieDf,ratingDf = movieInput()
        movieDf = movieDf.iloc[:1]
        #st.write(movieDf.columns.tolist())
        
        a = movieDf['Poster'].to_list()
        b = movieDf['Title'].to_list()
        st.markdown("----")
        st.header("About")
        col1, col2 = st.beta_columns(2)
        col1.image(a, caption=b)
        col2.write("Name : " + b[0])
        col2.markdown("<br>",unsafe_allow_html=True)
        col2.write("Year : " + (movieDf['Year'].to_list())[0])
        col2.markdown("<br>",unsafe_allow_html=True)
        col2.write("Release Date : " + (movieDf['Released'].to_list())[0])
        col2.markdown("<br>",unsafe_allow_html=True)
        col2.write("Run Time : " + (movieDf['Runtime'].to_list())[0])
        col2.markdown("<br>",unsafe_allow_html=True)
        col2.write("IMDb Rating : " + (movieDf['imdbRating'].to_list())[0])
        col2.markdown("<br>",unsafe_allow_html=True)
        col2.write("Earnings on Box Office : " + (movieDf['BoxOffice'].to_list())[0])
        col2.markdown("<br>",unsafe_allow_html=True)
        col2.write("Actors : " + (movieDf['Actors'].to_list())[0])
        st.markdown("---")
        
        st.header("Detailed Info.")
        newMovieDf = movieDf[['Title','Rated','Genre','Language','Country','Type','Production','imdbID','Director','Writer','Awards']]
        st.write(newMovieDf.transpose().style.set_properties(**{'background-color': 'Turquoise'}))
        st.subheader("Ratings")
        st.write((ratingDf.transpose()).style.set_properties(**{'background-color': 'DarkTurquoise'}))
        st.subheader("Plot")
        st.info((movieDf['Plot'].to_list())[0])
        st.markdown("---")
        
        st.header("Similar Movies")
        similarList = similarMovies(b)
        st.write(similarList)
        
    except:
        pass
    



def get_movies_from_tastedive(input_title):
    base_url = 'https://tastedive.com/api/similar'
    param_d = {}
    param_d['q'] = input_title
    #param_d['limit'] = 5
    param_d['type'] = 'movies'
    response = requests.get(base_url, params = param_d)
    response_d=response.json()
    return response_d

def similarMovies(inputMovie):
    a = get_movies_from_tastedive(inputMovie)
    a = a['Similar']['Results']
    df = pd.DataFrame(a)
    similarList = df['Name'].to_list()
    return similarList
    


def compareTwoMovies():
    mlist = twoMovieinput()
    try:
        for i in range(2):
            if i ==0:
                inputInfo = urlGenerator(mlist[i])
                mdf1,rdf1 = movieDataGenerator(inputInfo)
            if i == 1:
                inputInfo = urlGenerator(mlist[i])
                mdf2,rdf2 = movieDataGenerator(inputInfo)
                
        mdf1 = mdf1.iloc[:1]
        mdf2 = mdf2.iloc[:1]
        #st.write(mdf2.columns.tolist())
        
        a = mdf1['Poster'].to_list()
        b = mdf1['Title'].to_list()
        c = mdf2['Poster'].to_list()
        d = mdf2['Title'].to_list()
        
        st.markdown("---")
        
        col1, col2 = st.beta_columns(2)
        col1.image(a, caption=b)
        col2.image(c, caption=d)
        
        st.markdown("---")
        
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Title : ")
        col2.write(b[0])
        col3.write(d[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("IMDb Rating : ")
        col2.write((mdf1['imdbRating'].to_list())[0])
        col3.write((mdf2['imdbRating'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Runtime : ")
        col2.write((mdf1['Runtime'].to_list())[0])
        col3.write((mdf2['Runtime'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Year : ")
        col2.write((mdf1['Year'].to_list())[0])
        col3.write((mdf2['Year'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Release Date : ")
        col2.write((mdf1['Released'].to_list())[0])
        col3.write((mdf2['Released'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("BoxOffice : ")
        col2.write((mdf1['BoxOffice'].to_list())[0])
        col3.write((mdf2['BoxOffice'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Language : ")
        col2.write((mdf1['Language'].to_list())[0])
        col3.write((mdf2['Language'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Country : ")
        col2.write((mdf1['Country'].to_list())[0])
        col3.write((mdf2['Country'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Actors : ")
        col2.write((mdf1['Actors'].to_list())[0])
        col3.write((mdf2['Actors'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Awards : ")
        col2.write((mdf1['Awards'].to_list())[0])
        col3.write((mdf2['Awards'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Plot : ")
        col2.write((mdf1['Plot'].to_list())[0])
        col3.write((mdf2['Plot'].to_list())[0])

    except:
        pass


def movies():
    activities = ['Analyse a Movie', 'Compare Two Movies'] # CHOOSE EITHER ONE
    choice = st.selectbox("Analyse or Compare", activities)
    
    if choice == 'Analyse a Movie':
        movieAnalysis()
        
    if choice == 'Compare Two Movies':
        compareTwoMovies()


        
def seriesAnalysis():
    try:
        seriesDf,ratingDf = seriesInput()
        seriesDf = seriesDf.iloc[:1]
        #st.write(seriesDf.columns.tolist())
        
        a = seriesDf['Poster'].to_list()
        b = seriesDf['Title'].to_list()
        st.markdown("----")
        st.header("About")
        col1, col2 = st.beta_columns(2)
        col1.image(a, caption=b)
        col2.write("Name : " + b[0])
        col2.markdown("<br>",unsafe_allow_html=True)
        col2.write("Total Seasons : " + (seriesDf['totalSeasons'].to_list())[0])
        col2.markdown("<br>",unsafe_allow_html=True)
        col2.write("Year : " + (seriesDf['Year'].to_list())[0])
        col2.markdown("<br>",unsafe_allow_html=True)
        col2.write("Release Date : " + (seriesDf['Released'].to_list())[0])
        col2.markdown("<br>",unsafe_allow_html=True)
        col2.write("Avg. Episodes Run Time : " + (seriesDf['Runtime'].to_list())[0])
        col2.markdown("<br>",unsafe_allow_html=True)
        col2.write("IMDb Rating : " + (seriesDf['imdbRating'].to_list())[0])
        col2.markdown("<br>",unsafe_allow_html=True)
        col2.write("Actors : " + (seriesDf['Actors'].to_list())[0])
        st.markdown("---")
        
        st.header("Detailed Info.")
        newSeriesDf = seriesDf[['Title','Rated','Genre','Language','Country','Type','imdbID','Director','Writer','Awards']]
        st.write(newSeriesDf.transpose().style.set_properties(**{'background-color': 'Turquoise'}))
        st.subheader("Ratings")
        st.write((ratingDf.transpose()).style.set_properties(**{'background-color': 'DarkTurquoise'}))
        st.subheader("Plot")
        st.info((seriesDf['Plot'].to_list())[0])
        st.markdown("---")
        
        st.header("Similar Series")
        st.warning('May contain unrelated recommendation , will fix this later :(')
        similarList = similarSeries(b)
        st.write(similarList)
        
    except:
        pass


def get_series_from_tastedive(input_title):
    base_url = 'https://tastedive.com/api/similar'
    param_d = {}
    param_d['q'] = input_title
    #param_d['limit'] = 5
    param_d['type'] = 'series'
    response = requests.get(base_url, params = param_d)
    response_d=response.json()
    return response_d

def similarSeries(inputSeries):
    a = get_series_from_tastedive(inputSeries)
    a = a['Similar']['Results']
    df = pd.DataFrame(a)
    similarList = df['Name'].to_list()
    return similarList


def compareTwoSeries():
    mlist = twoSeriesinput()
    try:
        for i in range(2):
            if i ==0:
                inputInfo = urlGenerator(mlist[i])
                mdf1,rdf1 = seriesDataGenerator(inputInfo)
            if i == 1:
                inputInfo = urlGenerator(mlist[i])
                mdf2,rdf2 = seriesDataGenerator(inputInfo)
                
        mdf1 = mdf1.iloc[:1]
        mdf2 = mdf2.iloc[:1]
        #st.write(mdf2.columns.tolist())
        
        a = mdf1['Poster'].to_list()
        b = mdf1['Title'].to_list()
        c = mdf2['Poster'].to_list()
        d = mdf2['Title'].to_list()
        
        st.markdown("---")
        
        col1, col2 = st.beta_columns(2)
        col1.image(a, caption=b)
        col2.image(c, caption=d)
        st.markdown("---")
        
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Title : ")
        col2.write(b[0])
        col3.write(d[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("IMDb Rating : ")
        col2.write((mdf1['imdbRating'].to_list())[0])
        col3.write((mdf2['imdbRating'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Avg. Runtime : ")
        col2.write((mdf1['Runtime'].to_list())[0])
        col3.write((mdf2['Runtime'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Year : ")
        col2.write((mdf1['Year'].to_list())[0])
        col3.write((mdf2['Year'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Release Date : ")
        col2.write((mdf1['Released'].to_list())[0])
        col3.write((mdf2['Released'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Seasons : ")
        col2.write((mdf1['totalSeasons'].to_list())[0])
        col3.write((mdf2['totalSeasons'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Language : ")
        col2.write((mdf1['Language'].to_list())[0])
        col3.write((mdf2['Language'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Country : ")
        col2.write((mdf1['Country'].to_list())[0])
        col3.write((mdf2['Country'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Actors : ")
        col2.write((mdf1['Actors'].to_list())[0])
        col3.write((mdf2['Actors'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Awards : ")
        col2.write((mdf1['Awards'].to_list())[0])
        col3.write((mdf2['Awards'].to_list())[0])
        
        st.markdown("---")
        col1, col2, col3 = st.beta_columns(3)
        col1.write("Plot : ")
        col2.write((mdf1['Plot'].to_list())[0])
        col3.write((mdf2['Plot'].to_list())[0])

        
    except:
        pass


def series():
    activities = ['Analyse a Series', 'Compare Two Series'] # CHOOSE EITHER ONE
    choice = st.selectbox("Analyse or Compare", activities)
    
    if choice == 'Analyse a Series':
        seriesAnalysis()
        
    if choice == 'Compare Two Series':
        compareTwoSeries()



def sidebarfunction(): #CREATING A BAR NAVIGATION FORM
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    link1 = '[movieXplore Repository](https://github.com/305kishan/movieXplore)'
    link2 = '[How it works?](https://github.com/305kishan/movieXplore/blob/main/README.md)'
    st.sidebar.markdown(link1, unsafe_allow_html=True)
    st.sidebar.markdown(link2, unsafe_allow_html=True)
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.write("Reach Me Here!")
    link = '[GitHub](https://github.com/305kishan)'
    st.sidebar.markdown(link, unsafe_allow_html=True)
    link = '[Kaggle](https://www.kaggle.com/kishan305)'
    st.sidebar.markdown(link, unsafe_allow_html=True)
    link = '[LinkedIn](https://www.linkedin.com/in/305kishan/)'
    st.sidebar.markdown(link, unsafe_allow_html=True)
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)



def main():
    
    st.title("movieXplore")
    st.markdown('<style>h1{color: red;}</style>',unsafe_allow_html=True)
    st.markdown('Get Information about movies or series, see similar titles and compare them')
    st.markdown("******")
    
    sidebarfunction()
    
    activities = ['Movies', 'Series'] # CHOOSE EITHER ONE
    choice = st.selectbox("Select", activities)
    
    if choice =='Movies':
        movies()
        
    if choice =='Series':
        series()

    

if __name__=="__main__":
    main()