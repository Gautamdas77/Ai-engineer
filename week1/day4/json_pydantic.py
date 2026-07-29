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

#structure it
from pydantic import BaseModel
class Ticket(BaseModel):
    name:str
    email:str
    issue:str
    number:int

schema=Ticket.model_json_schema()
response_format={
    "type":"json_object"
}

system_prompt=f"""
Extract the personal information form the ticket strictly based on this schema and give me a json output.
{schema}
"""

message_system={
    "role": "system",
    "content": system_prompt
}

text = "Helo my name is gautam. I have an iphone which is not working at all. My address is delhi. My emial is abc@gmail.com. My contacty number is 82511."
prompt = f"""
You are a data extraction expert. You will be given a text and you have to extract the following information from it:{text}
"""

message = {
    "role":role,
    "content":prompt
}

messages = [message_system,message]

response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)
answer = response.choices[0].message.content
print (answer)

#isko padhte kaise hai
import json
raw_json=answer
data_files=json.loads(raw_json)
ticket=Ticket(**data_files)

print(ticket.name)
print(ticket.email)
print(ticket.issue)
print(ticket.number)

