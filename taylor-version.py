import pandas as pd
import streamlit as st
import plotly.express as px

st.title('Taylor Swift App')

#--- IMPORT DATA ---#
DATA_URL="spotify_taylorswift.csv"

#--- SHOW DATABASE ---#
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL,nrows=nrows ,index_col=0, encoding='latin-1')
    return data

#--- FILTER DATA ---#
def load_data_byname(name):
    data = pd.read_csv(DATA_URL,index_col=0, encoding='latin-1')
    filtered_data_byname = data[data["name"].str.contains(name, case = False)]
    return filtered_data_byname

def load_data_byalbum(album):
    data = pd.read_csv(DATA_URL, index_col=0, encoding='latin-1')
    filtered_data_byalbum = data[data[ "album" ] == album]
    return filtered_data_byalbum

#--- MAIN CONFIG ---#
data_load_state = st.text('Developed by Lilliam Romero Reyes')
data_load_state = st.caption('Application that gathers and graphically represents data on Taylor Swifts discography from her first debut album "Taylor Swift" to her latest release Fearless (Taylors Version), then April 2021, showing the most relevant data on each of her songs')
data = load_data(100)
st.header("Taylor Swift song database")

#--- LOGO ---#
st.sidebar.image("taylor-logo.jfif")
st.sidebar.markdown("##")

#--- SIDEBAR ---#

sidebar = st.sidebar
agree = sidebar.checkbox("Show database")
if agree:
    st.dataframe(data)

myname = sidebar.text_input('Song title :')
btnRange = sidebar.button('Search song')

#--- INFORMATION SEARCH ---#
if (myname):
    if (btnRange):
        filterbyname = load_data_byname(myname)
        count_row = filterbyname.shape[0]
        st.header("Search result: ")
        st.dataframe(filterbyname)
        st.write(f"Search songs : {count_row}")

selected_album = sidebar.selectbox("Choose an album: ", data ['album'].unique())
btnFilterbyAlbum = sidebar.button('Filter album')

if (btnFilterbyAlbum):
    filterbyAlbum = load_data_byalbum(selected_album)
    count_row = filterbyAlbum.shape[0]
    st.header("Search result: ")
    st.dataframe(filterbyAlbum)
    st.write(f"Total items : {count_row}")

    
#--- SIDEBAR FILTERS ---#
popularity = st.sidebar.multiselect("Select range of popularity of a song",
                                    options=data['popularity'].unique(),
                                    default=data['popularity'].unique())

danceability = st.sidebar.multiselect("Select danceability",
                                    options=data['danceability'].unique(),
                                    default=data['danceability'].unique())
st.sidebar.markdown("##")

data_selection = data.query("popularity == @popularity & danceability == @danceability")
#--- CHARTS ---#

#Chart to visualize the popularity of a song 
name = data_selection['name']
popularity_song = data_selection['popularity']

fig_popularity = px.bar(data_selection,
                            x=name,
                            y = popularity_song,
                            title = "Popularity of songs",
                            labels=dict(name="Name of song",
popularity="Popularity of a song"),
                            color_discrete_sequence=["#FE0000"],
                            template="plotly_white")
fig_popularity.update_layout(plot_bgcolor="rgba(254, 0, 0 )")
st.plotly_chart(fig_popularity)

data_load_state = st.caption('Histogram of ercent popularity of the song based on Spotifys algorithm (possibly the number of stream at a certain period of time)')

#Chart to visualize the danceability of a song
dance_song = (
    data_selection.groupby(by=['danceability']).sum()
    [['length']].sort_values(by="length"))

bar_char_dance=px.bar(dance_song,
                    x = dance_song.index,
                    y = "length",
                    orientation="v",
                    title="The danceability of a song by length",
                    labels=dict(danceabili="length", danceability="danceability"),
                    color_discrete_sequence=["#FE0000"],
                    template="plotly_white")

bar_char_dance.update_layout(plot_bgcolor="rgba(254, 0, 0)")
st.plotly_chart(bar_char_dance)

data_load_state = st.caption('Bar chart that measures how suitable a track is for dancing based on a combination of musical elements including tempo, beat stability, time signature; comparing song length in milliseconds')

#Chart to visualize the valence by energy in every album
energy = data_selection['energy']
album = data_selection['album']
valence = data_selection['valence']
fig_energy=px.scatter(data_selection,
                    x = energy,
                    y = valence,
                    color = album,
                    title = "The energy by valence in every album",
                    labels=dict(energy="Energy", valence="Valence", album="Album"),
                    template="plotly_white")
fig_energy.update_layout(plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_energy)

data_load_state = st.caption('Scatter plot representing the energy (a perceptual measure of intensity and activity) and valence (a measure of how happy or sad the song sounds) of each album')