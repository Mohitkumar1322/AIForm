from flask import Flask, request, jsonify, render_template, send_file
import cohere
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Load system prompt
with open("prompt_template.txt", "r") as f:
    system_prompt = f.read()

EXCEL_FILE = "data.xlsx"

# Home Route
@app.route("/")
def home():
    return render_template("index.html")

# Parse the form data
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

        result_text = response.generations[0].text.strip()

        # Try converting the result into a dict
        lines = result_text.split("\n")
        parsed_dict = {}
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                parsed_dict[key.strip()] = value.strip()

        # Append to Excel
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
            df = pd.concat([df, pd.DataFrame([parsed_dict])], ignore_index=True)
        else:
            df = pd.DataFrame([parsed_dict])
        df.to_excel(EXCEL_FILE, index=False)

        return jsonify({
            "status": "success",
            "result": result_text
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Endpoint to download the Excel file
@app.route("/download", methods=["GET"])
def download_excel():
    if os.path.exists(EXCEL_FILE):
        return send_file(EXCEL_FILE, as_attachment=True)
    return jsonify({"error": "Excel file not found."}), 404

if __name__ == "__main__":
    app.run(debug=True)
