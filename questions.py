from pymongo import MongoClient
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
#mongodb setup
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
db_name = os.getenv("DB_NAME")
db = client[db_name]
question_collection = db["questionnaire"]

def question_page():

    def get_next_question_id():
        counter = db.counters.find_one_and_update(
            {"_id": "question_id"},
            {"$inc": {"sequence_value": 1}},
            return_document=True,
            upsert=True
        )
        return counter["sequence_value"]

    with st.container():
            
            question_form = st.form("Fill out the details", clear_on_submit=True)
            with question_form:
                instruction = st.text_area("Enter the Instruction")
                ask_question = st.text_area("Enter the Question")
                type = st.selectbox("Question Type",("MCQs","True or False","Right or Wrong","Others"))
                options_raw = st.text_area("Enter the options (comma-separated)")
                options = [opt.strip() for opt in options_raw.split(",") if opt.strip()]

            
                submitted = st.form_submit_button("Submit Question",)

                if submitted:
                    if not ask_question or not options:
                        st.warning("Please enter both a question and at least one option.")
                    else:
                        question_id = get_next_question_id()
                        question_doc = {
                            "question_id": question_id,
                            "instruction": instruction,
                            "question": ask_question,
                            "type": type.lower().replace(" ", "_"),  # Normalize type
                            "options": options
                        }
                        question_collection.insert_one(question_doc)
                        st.success(f"✅ Question {question_id} saved successfully!")

                    
