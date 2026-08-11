import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("api key nahi mili")

client = Groq(api_key=my_api_key)
model = "llama-3.3-70b-versatile"

def llm_ans(prompt):
    message={
        "role": "user",
        "content": prompt
    }
    messages=[message]
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    ans = response.choices[0].message.content
    return ans

Good_prompt="""
#ROLE:
You are a support assistant mobile/laptop company
#TASK:
You have to classify the issue in a category
#CONSTRAINTS:
You have to classify the issue in one of three categories namely billing, technical, return
#OUTPUT FORMAT:
Your output should be only in one word only. The one word should be one of the categories given in constraints
#EXAMPLE:
For instance if a user complain says he wants a refund then the catogory is Return
#FALLBACK:
If the issue is unrelated to any of the categories mentioned in the constraints then you have to say "unrelated"
This is a user complaint:
My laptop is not working
classify this
"""


print(llm_ans(Good_prompt))