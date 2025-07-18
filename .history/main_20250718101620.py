from flask import Flask, request, jsonify
import cohere
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key)

# Load system prompt
with open("prompt_template.txt", "r") as f:
    system_prompt = f.read()

# Initialize Flask App
app = Flask(__name__)

@app.route("/parse-form", methods=["POST"])
def parse_form():
    try:
        data = request.get_json()
        user_prompt = data.get("prompt", "")
        full_prompt = f"{system_prompt}\n\nUser Input:\n{user_prompt}"
        
        response = co.generate(
            model='command-r-plus',
            prompt=full_prompt,
            max_tokens=300,
            temperature=0.2
        )

        return jsonify({
            "status": "success",
            "result": response.generations[0].text.strip()
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
