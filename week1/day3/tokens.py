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
role = "user"
# 3 prompt
prompt1 = "Hi!"
prompt2 = "Explain time travel in Detail"
prompt3 = "write a 1000 word essay on machine learning"

prompts = [prompt1, prompt2, prompt3]

for prompt in prompts:
    message = {
    "role":role,
    "content":prompt
    }
    messages = [message]
    response = client.chat.completions.create(model=model, messages=messages, max_tokens=50)
    usage=response.usage
    print(f"Prompt: {prompt}-->Your tokens:{usage.prompt_tokens}, Completion tokens:{usage.completion_tokens}, Total tokens:{usage.total_tokens} Finish Reason: {response.choices[0].finish_reason}")
    # prompt = "Do you know pratyush?"

    # message = {
    #     "role":role,
    #     "content":prompt
    # }

    # messages = [message]

    # response = client.chat.completions.create(model=model, messages=messages, temperature=2)
answer = response.choices[0].message.content
print (answer)