import cohere
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("COHERE_API_KEY")

co = cohere.Client(api_key)

with open("prompt_template.txt", "r") as f:
    system_prompt = f.read()

user_input = """
Hi, I’m Mohit Kumar. I want to apply for Backend Developer. My email is mohit@gmail.com, phone is 9876543210, and LinkedIn is linkedin.com/in/mohitkumar.
"""

full_prompt = system_prompt + "\n\nUser Input:\n" + user_input

response = co.generate(
    model='command-r-plus',
    prompt=full_prompt,
    max_tokens=300,
    temperature=0.2
)

print(response.generations[0].text.strip())
