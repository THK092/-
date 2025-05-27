import streamlit as st
import requests

# TMDB API 키 설정
TMDB_API_KEY = '여기에_본인의_API_KEY_입력'

def search_movie(title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            return results[0]  # 첫 번째 결과 반환
    return None

def get_poster_url(poster_path):
    return f"https://image.tmdb.org/t/p/w500{poster_path}"

# Streamlit UI
st.title("🎬 영화 정보 검색기")
movie_title = st.text_input("영화 제목을 입력하세요")

if movie_title:
    movie = search_movie(movie_title)
    if movie:
        st.header(movie['title'])
        st.image(get_poster_url(movie['poster_path']))
        st.subheader("줄거리")
        st.write(movie.get('overview', '줄거리 없음'))
        st.write(f"📅 개봉일: {movie.get('release_date', '정보 없음')}")
        st.write(f"⭐ 평점: {movie.get('vote_average', '없음')}점")
    else:
        st.warning("영화를 찾을 수 없습니다.")
