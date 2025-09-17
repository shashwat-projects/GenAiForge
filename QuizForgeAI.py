import os
import pandas as pd
import warnings
import json
import streamlit as st
from src.quizforgeai.logger import logging
from src.quizforgeai.utils import read_file, convert_to_pandasdf
from src.quizforgeai.quizforgeai import generate_evaluate_chain 

warnings.filterwarnings("ignore")

with open(r"response.json", "r") as file:
    response = json.load(file)


st.set_page_config(
    page_title="QuizForge AI",
    page_icon="🧠",
    layout="wide",
)


st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #4e54c8, #8f94fb);
            background-attachment: fixed;
        }
        .main-title {
            font-size: 2.8rem;
            font-weight: 800;
            text-align: center;
            color: #ffffff;
            margin-bottom: 5px;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
        }
        .subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #f1f1f1;
            margin-bottom: 40px;
        }
        .stForm {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 14px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.15);
        }
        .mcq-card {
            background: #ffffff;
            border-radius: 14px;
            overflow: hidden;
            margin-bottom: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .mcq-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.25);
        }
        .mcq-header {
            background: linear-gradient(90deg, #4e54c8, #8f94fb);
            color: white;
            font-weight: 700;
            font-size: 1.1rem;
            padding: 12px 16px;
        }
        .mcq-body {
            padding: 18px;
        }
        .mcq-question {
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 12px;
            font-size: 1.05rem;
        }
        .mcq-option {
            margin-left: 15px;
            color: #444;
            margin-bottom: 6px;
        }
        .correct {
            color: #27ae60;
            font-weight: 600;
            margin-top: 10px;
        }
        .review-card {
            background: #ffffff;
            border-radius: 14px;
            overflow: hidden;
            margin-top: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .review-header {
            background: linear-gradient(90deg, #4e54c8, #8f94fb);
            color: white;
            font-weight: 700;
            font-size: 1.1rem;
            padding: 12px 16px;
        }
        .review-body {
            padding: 18px;
            color: #2c3e50;
            font-size: 1rem;
        }
        .section-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #ffffff;
            margin: 30px 0 15px 0;
        }
        /* Custom buttons */
        .stDownloadButton > button, .stFormSubmitButton > button {
            background: linear-gradient(90deg, #4e54c8, #8f94fb);
            color: white;
            font-weight: 600;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            border: none;
            box-shadow: 0px 3px 6px rgba(0,0,0,0.2);
            transition: 0.2s ease-in-out;
        }
        .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {
            background: linear-gradient(90deg, #5d63d4, #9a9efc);
            transform: scale(1.03);
            box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        }
        /* Input labels */
        label {
            font-weight: 600 !important;
            color: #2c3e50 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- HEADER ----------
st.markdown('<div class="main-title">🧠 QuizForge AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Turn your study materials into smart MCQs instantly</div>', unsafe_allow_html=True)

# ---------- FORM ----------
with st.form("mcq_form"):
    uploaded_file = st.file_uploader("📂 Upload a PDF or Text file")
    number_of_questions = st.number_input("🔢 Number of Questions", min_value=3, max_value=30, value=5)
    subject = st.text_input("📘 Subject", max_chars=200)
    level = st.selectbox("🎯 Difficulty Level", options=["Easy", "Medium", "Hard"], index=0)
    submit_button = st.form_submit_button("✨ Generate Quiz")

# ---------- QUIZ GENERATION ----------
if submit_button and uploaded_file is not None and number_of_questions and subject and level:
    try:
        file_text = read_file(uploaded_file)
        logging.info("File read successfully.")
       
        result = generate_evaluate_chain(
            {
                "text": file_text,
                "number": number_of_questions,
                "subject": subject,
                "level": level,
                "response_json": json.dumps(response),
            }
        )

        quiz_dict = result["quiz"]
        review_dict = result["review"]

        if quiz_dict:
            st.markdown('<div class="section-title">📝 Generated MCQs</div>', unsafe_allow_html=True)
            for q_num, q_data in quiz_dict.items():
                st.markdown(
                    f"""
                    <div class="mcq-card">
                        <div class="mcq-header">Question {q_num}</div>
                        <div class="mcq-body">
                            <div class="mcq-question">{q_data['mcq']}</div>
                            <div class="mcq-option">A) {q_data['options']['a']}</div>
                            <div class="mcq-option">B) {q_data['options']['b']}</div>
                            <div class="mcq-option">C) {q_data['options']['c']}</div>
                            <div class="mcq-option">D) {q_data['options']['d']}</div>
                            <div class="correct">✅ Correct Answer: {q_data['correct'].upper()}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            logging.info("MCQs generated and displayed successfully.")

            # Downloads
            st.markdown('<div class="section-title">📥 Download Quiz</div>', unsafe_allow_html=True)
            quiz_json = json.dumps(quiz_dict, indent=4)
            st.download_button(
                label="💾 Download as JSON",
                data=quiz_json,
                file_name="quiz.json",
                mime="application/json",
            )

            quiz_df = convert_to_pandasdf(quiz_dict)
            csv_data = quiz_df.to_csv(index=False)
            st.download_button(
                label="📊 Download as CSV",
                data=csv_data,
                file_name="quiz.csv",
                mime="text/csv",
            )

        else:
            st.error("❌ Failed to generate quiz questions.")

        # Evaluation box
        st.markdown('<div class="section-title">🧐 Quiz Evaluation</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="review-card">
                <div class="review-header">Evaluation</div>
                <div class="review-body">{review_dict}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        logging.info("Quiz evaluation displayed successfully.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")