from pymongo import MongoClient
import streamlit as st
from dotenv import load_dotenv
import os
from questions import *

# Load environment variables
load_dotenv()
#mongodb setup
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
db_name = os.getenv("DB_NAME")
db = client[db_name]

def screening():
    with st.container():
        if "question_index" not in st.session_state:
            screening_form = st.form("Screening Form")
            with screening_form:
                st.caption("Let's start the Screening Test. Read all the instructions carefully.")
                submitted = st.form_submit_button("Start")
                if submitted:
                    st.session_state.question_index = 0

        if "question_index" in st.session_state:
            questions = list(question_collection.find().sort("question_id", 1))
            if st.session_state.question_index < len(questions):
                current_question = questions[st.session_state.question_index]
                st.markdown(f"### Q{current_question['question_id']}: {current_question['question']}")
                st.caption(current_question.get("instruction", ""))

                st.radio("Choose one:", current_question["options"], key=current_question["question_id"])

                if st.button("Next"):
                    st.session_state.question_index += 1
                if st.button("Previous"):
                    if st.session_state.question_index > 0:
                        st.session_state.question_index -=1
            else:
                st.success("✅ You've completed all questions!")
                del st.session_state.question_index