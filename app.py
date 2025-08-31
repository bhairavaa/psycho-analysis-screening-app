import streamlit as st
from questions import question_page
from screening import screening


st.set_page_config("Psycho Analysis Screening App")
with st.container():
    st.markdown("""
        <h1 style='text-align:center;'>
                <span style='color: #640704;'>Psycho Analysis <span>
                <span style='color: #080A43;'>Screening App<span>
        </h1>
        """,unsafe_allow_html=True)

if "screen" not in st.session_state:
    st.session_state.screen= "home"

with st.sidebar:
    
    if st.button("Go To Home"):
        st.session_state.screen = "home"
    if st.button("Add Question"):
        st.session_state.screen = "questions"
    if st.button("Screening Test"):
        st.session_state.screen = "screening"

if st.session_state.screen == "home":
    st.caption("Welcome")

elif st.session_state.screen == "questions":
    question_page()
elif st.session_state.screen == "screening":

    screening()

