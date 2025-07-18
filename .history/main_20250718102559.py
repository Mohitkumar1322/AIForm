from flask import Flask, request, jsonify
import cohere
from dotenv import load_dotenv
import os

# Load environment variables (e.g., API key from .env file)
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")

# Initialize Cohere client
co = cohere.Client(api_key)

# Load the system prompt template from file
with open("prompt_template.txt", "r") as f:
    system_prompt = f.read()

# Initialize Flask app
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Welcome to the AI Form Parser API!"})

@app.route("/parse-form", methods=["POST"])
def parse_form():
    try:
        # Get JSON payload from the request
        data = request.get_json()
        user_prompt = data.get("prompt", "").strip()

        # Construct the full prompt using the system template
        full_prompt = f"{system_prompt}\n\nUser Input:\n{user_prompt}"

        # Call Cohere model
        response = co.generate(
            model='command-r-plus',
            prompt=full_prompt,
            max_tokens=300,
            temperature=0.2
        )

        # Extract result and return
        result_text = response.generations[0].text.strip()
        return jsonify({
            "status": "success",
            "result": result_text
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
