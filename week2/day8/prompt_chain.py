import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from time import sleep

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("api key nahi mili")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"

JD = """
We are hiring a Backend python developer.

Requirements:
- strong python
- fastapi or Django
- postgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""

RESUME = """
Name : Gautam Das
skills: 
- python
- fastapi
- docker
- mysql
- node js
- git
experience:
backend engineer in meta for past 4 years
"""


def ask_llm(system_prompt, user_prompt):
    sys_msg = {
        "role": "system",
        "content": system_prompt
    }

    user_msg = {
        "role": "user",
        "content": user_prompt
    }

    messages = [sys_msg, user_msg]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    answer = response.choices[0].message.content
    return answer


def step1_resume_extract():
    system_prompt = """
    You are an expert Hr asistant with an exerince of 20+ years in this field , your 
    task is to extract the name,skills and experience from the resume. dont give any unnessary
    details and dont generate anything on your own just return the extracted data
    output format: give skills in comma seperated values, 
    experience in years, if experience is not present in resume return 0 years
    """
    user_prompt = f"""
    Here is the resume:
    {RESUME}
    """

    return ask_llm(system_prompt, user_prompt)


def step2_JD_extract():
    system_prompt = """
    You are an expert Hr asistant with an exerince of 20+ years in this field , your 
    task is to extract the skills and experience from the JD. dont give any unnessary
    details and dont generate anything on your own just return the extracted data
    output format: give skills in comma seperated values, 
    experience in years
    """
    user_prompt = f"""
    Here is the JD:
    {JD}
    """

    return ask_llm(system_prompt, user_prompt)


def step3_match_resume_jd(resume, jd):
    system_prompt = """
    You are an expert Hr asistant with an exerince of 20+ years in this field , your 
    task is to match the resume with the JD. dont give any unnessary
    details and dont generate anything on your own , just compare the resume and jd 
    and give a score out of 1 - 100 from the perspective of JD and also give a little bit of reasoning for that score
    output format: 
    score: 
    reasoning: 
    """
    user_prompt = f"""
    Here is the resume:
    {resume}
    
    Here is the JD:
    {jd}
    """

    return ask_llm(system_prompt,user_prompt)


candidate = step1_resume_extract()
print(candidate)
sleep(2)
job = step2_JD_extract()
print(job)
sleep(2)
match = step3_match_resume_jd(candidate,job)
print(match)