import streamlit as st
import requests

# TMDB API 키를 입력하세요 (https://www.themoviedb.org/ 에서 발급 가능)
TMDB_API_KEY = 'YOUR_TMDB_API_KEY_HERE'

# 영화 검색 함수
def search_movie(title):
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': title,
        'language': 'ko-KR'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            return results[0]  # 첫 번째 결과 반환
    return None

# 포스터 URL 생성 함수
def get_poster_url(poster_path):
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

# Streamlit UI 구성
st.set_page_config(page_title="영화 정보 검색기", page_icon="🎬")
st.title("🎬 영화 정보 검색기")

movie_title = st.text_input("🔍 영화 제목을 입력하세요:")

if movie_title:
    with st.spinner("영화 정보를 검색 중입니다..."):
        movie = search_movie(movie_title)

    if movie:
        st.success(f"\"{movie['title']}\" 검색 성공!")

        # 포스터
        poster_url = get_poster_url(movie.get('poster_path'))
        if poster_url:
            st.image(poster_url, use_column_width=True)

        # 영화 기본 정보
        st.subheader("📄 줄거리")
        st.write(movie.get('overview', '줄거리 정보가 없습니다.'))

        st.subheader("📅 개봉일")
        st.write(movie.get('release_date', '정보 없음'))

        st.subheader("⭐ 평점")
        st.write(f"{movie.get('vote_average', 0)} / 10")
    else:
        st.error("❌ 영화를 찾을 수 없습니다. 다른 제목을 입력해보세요.")
