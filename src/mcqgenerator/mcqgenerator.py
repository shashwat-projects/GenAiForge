import os
import pandas as pd
import warnings
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain_core.output_parsers import JsonOutputParser
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file, convert_to_pandasdf

warnings.filterwarnings("ignore")

load_dotenv()

os.getenv("HUGGINGFACEHUB_API_TOKEN")

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V3.1",
)

# Here, llm is not a normal text LLM, it’s a chat LLM as deepseek-ai/DeepSeek-V3.1 doesnt support text but only conversation— so LLMChain doesn’t really know how to talk to it. That’s why I have used ChatHuggingFace, which wraps HuggingFaceEndpoint and converts it into something LLMChain can understand.

chat_model = ChatHuggingFace(llm=llm)

# Quiz Generation

quiz_generation_template="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students with difficulty level {level}. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""
quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "level", "response_json"],
    template=quiz_generation_template
    )
quiz_chain=LLMChain(llm=chat_model, prompt=quiz_generation_prompt, output_key="quiz", output_parser= JsonOutputParser(), verbose=True)

# Quiz Evaluation

quiz_evaluation_template="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""
quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=quiz_evaluation_template)
review_chain=LLMChain(llm=chat_model, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

# Combined Chain
generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "subject", "level", "response_json"], output_variables=["quiz", "review"], verbose=True,)


