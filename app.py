import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(layout="wide")
def fetch_poster_page(kdrama_id):
    response = requests.get(
        'https://api.themoviedb.org/3/tv/{}?api_key=e078ce48c8a8319e3d91498c283335bb&&language=en-US'.format(kdrama_id))
    data = response.json()

    if 'poster_path' in data and data['poster_path'] is not None:
        poster_url = "https://image.tmdb.org/t/p/original" + data['poster_path']
    else:
        poster_url = None

    if 'homepage' in data and data['homepage'] is not None:
        homepage_url = data['homepage']
    else:
        homepage_url = None

    return poster_url, homepage_url


def recommend(kdrama_selected):
    kd_index = kdramas[kdramas['Name'] == kdrama_selected].index
    if len(kd_index) == 0:
        st.error("Kdrama not found!")
        return [], [], []

    kd_index = kd_index[0]
    if kd_index >= len(similarity):
        st.error("Invalid kdrama index!")
        return [], [], []

    distances = similarity[kd_index]
    kd_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_kdramas = []
    recommend_kdramas_poster = []
    recommend_kdramas_homepage = []
    for i in kd_list:
        kdrama_id = kdramas.iloc[i[0]].id
        recommend_kdramas.append(kdramas.iloc[i[0]].Name)
        poster, homepage = fetch_poster_page(kdrama_id)
        recommend_kdramas_poster.append(poster)
        recommend_kdramas_homepage.append(homepage)
    return recommend_kdramas, recommend_kdramas_poster, recommend_kdramas_homepage




kdramas_list = pickle.load(open('kdramas_dict.pkl', 'rb'))
kdramas = pd.DataFrame(kdramas_list)
kdramas.drop(236, axis=0, inplace=True)
similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('KChingu')
kdrama_selected = st.selectbox(
    'Select the Kdrama you have watched', kdramas['Name'])

if st.button('Recommend'):
    names,posters,homepage = recommend(kdrama_selected)

    # Create two columns
    col1, col2, col3,col4,col5 = st.columns(5)

    # In col1, display the image with a URL
    with col1:
        st.text(names[0])
        st.markdown('<a href="'+homepage[0]+'"><img src="'+posters[0]+'" width="200" ></a>', unsafe_allow_html=True)


    # In col2, display the image with a URL
    with col2:
        st.text(names[1])
        st.markdown('<a href="' + homepage[1] + '"><img src="' + posters[1] + '" width="200" ></a>',unsafe_allow_html=True)

    # In col3, display the image with a URL
    with col3:
        st.text(names[2])
        st.markdown('<a href="' + homepage[2] + '"><img src="' + posters[2] + '" width="200" ></a>', unsafe_allow_html=True)

    # In col3, display the image with a URL
    with col4:
        st.text(names[3])
        st.markdown('<a href="' + homepage[3] + '"><img src="' + posters[3] + '" width="200" ></a>',  unsafe_allow_html=True)

    # In col3, display the image with a URL
    with col5:
        st.text(names[4])
        st.markdown('<a href="' + homepage[4] + '"><img src="' + posters[4] + '" width="200" ></a>', unsafe_allow_html=True)


