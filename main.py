import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

# 네이버 영화 검색 함수
def get_movie_info_naver(query):
    search_url = f"https://movie.naver.com/movie/search/result.naver?query={urllib.parse.quote(query)}&section=all&ie=utf8"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # 첫 번째 영화 정보 추출
    result = soup.select_one("ul.search_list_1 li")

    if result:
        title = result.select_one(".result_thumb strong").text.strip()
        link = "https://movie.naver.com" + result.select_one("a")["href"]
        img = result.select_one("img")["src"]
        info_text = result.select_one(".result_info").text.strip()
        return {
            "title": title,
            "link": link,
            "img": img,
            "info": info_text
        }
    return None

# Streamlit UI
st.set_page_config(page_title="네이버 영화 검색기", page_icon="🎬")
st.title("🎬 네이버 영화 검색기")

query = st.text_input("🔍 영화 제목을 입력하세요:")

if query:
    with st.spinner("네이버 영화에서 정보를 가져오는 중..."):
        movie = get_movie_info_naver(query)

    if movie:
        st.success(f"✅ \"{movie['title']}\" 검색 성공!")
        st.image(movie["img"], width=300)
        st.subheader("📌 영화 정보")
        st.write(movie["info"])
        st.markdown(f"[🔗 네이버 영화 상세보기]({movie['link']})")
    else:
        st.error("❌ 결과를 찾을 수 없습니다. 다른 제목을 입력해보세요.")
