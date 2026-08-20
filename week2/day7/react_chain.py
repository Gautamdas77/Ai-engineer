import os
from pathlib import Path
from dotenv import load_dotenv
import groq
from groq import Groq
from time import sleep
import re

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("api key nahi mili")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"

#tools
def get_product_price(product):
    if product == 'iphone 17':
        return 1000
    elif product == 'iphone 15':
        return 500
    else:
        return 0


def calculator(expression):
    try:
        return eval(expression)
    except:
        return "calc error!"

tools = {
    "get_product_price": get_product_price,
    "calculator": calculator
}

system_prompt = """
You are a shopping assistant.

You have these tools:

get_product_price(product)
calculator(expression)
IMPORTANT:
call tools exactly ike these examples:

Action: get_product_price("iphone 17")
Action: calculator("2 + 2")

Never Write :
get_product_price(product="iphone 17")

Never write:
calculator(expression="2 + 2")

follow these rules:
2.Decide what you need to do next.
2.call only one tool at a time.
3.after writing an ation, stop immediately.
4.never guess or invent a tool result.
5.wait untill you receive an observation.
6.then decide you next action.
7.when the task is complete, give the final answer.

format:

Thoughts: what you need to do
Action: tool_name(argument)

when finished:

Final Answer: your answer
"""

def run_agent(question):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    for step in range(5):

        print("\n.....................")
        print("step", step + 1)
        print(".....................")

        response = client.chat.completions.create(model=model, messages=messages)

        answer = response.choices[0].message.content
        print(answer)

        #Agent has finished
        if "Final Answer:" in answer:
            break

        #Find the Action
        match = re.search(r"Action:\s*(\w+)\((.*)\)", answer)

        if match:
            tool_name = match.group(1)

            tool_input = match.group(2)

            tool_input = tool_input.strip()

            tool_input = tool_input.strip('"')

            #Run the tool
            if tool_name in tools:
                tool = tools[tool_name]
                observation = tool(tool_input)
            else:
                observation = "Tool not found!"

            print("Observation:", observation)

            #Add LLM response to memory
            messages.append({"role": "assistant", "content": answer})

            #Give tool result back to LLM
            messages.append({"role": "user", "content": "Observation: " + str(observation)})


prompt = """
I have 5000 rupees. What is the price of an iphone 17?
and how much money will i have left after buying it?
"""

run_agent(prompt)