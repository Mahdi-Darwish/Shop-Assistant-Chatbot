import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from app.core.config import Settings
from app.tools.products_tools import(get_products,search_product_by_name,get_products_by_max_price,get_products_by_min_price)
from app.tools_schema import tools
from app.tools_register import available_tools
from app.routes.chat_routes import SYSTEM_PROMPT
load_dotenv()
query = input('Type Something...')
MODEL_NAME = "openai/gpt-oss-120b"

# client = OpenAI(
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
#     api_key=os.getenv("GEMINI_API_KEY")
# )
# client = OpenAI(
#     base_url="http://localhost:11434/v1",
#     api_key="ollama",
# )
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=Settings.groq_api_key
)
messages = [
    {'role':'system','content':SYSTEM_PROMPT},
    {'role':'user','content':query},
]
# response = client.chat.completions.create(
#     model = 'gemini-3.1-flash-lite',
#     tools =tools,
#     messages=messages,
#     temperature=0.2
# )
# response = client.chat.completions.create(
#     model='llama3.1:8b',
#     tools=tools,
#     messages=messages,
#     temperature=0.2
# )
response = client.chat.completions.create(
    model = MODEL_NAME,
    tools=tools,
    messages=messages,
    temperature=0.2
)
if response.choices[0].message.tool_calls:
    messages.append(response.choices[0].message)
        # here the model will pick the suitable tool
    for tool_call in response.choices[0].message.tool_calls:
        tool_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        print("Tool selected:", tool_name)
        print("Arguments:", args)
        function = available_tools[tool_name]
        result = function(**args)
        print("Tool result:", result)
        messages.append({"role": "tool","tool_call_id": tool_call.id,"content": str(result)})
    # response2 = client.chat.completions.create(
    # model = 'gemini-3.1-flash-lite',
    # tools =tools,
    # messages=messages,
    # temperature=0.2
    # )
#     response2 = client.chat.completions.create(
#     model="qwen3:8b",
#     tools=tools,
#     messages=messages,
#     temperature=0.2
# )
        response2 = client.chat.completions.create(
        model=MODEL_NAME,
        tools=tools,
        messages=messages,
        temperature=0.2)
    print(response2.choices[0].message.content)
else:
     print(response.choices[0].message.content)




