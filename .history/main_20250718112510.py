from flask import Flask, request, jsonify, render_template, send_file
import cohere
from dotenv import load_dotenv
import os
import pandas as pd
from openpyxl import load_workbook

# Load environment variables
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key)

# Load system prompt
with open("prompt_template.txt", "r") as f:
    system_prompt = f.read()

# Flask App
app = Flask(__name__)

EXCEL_FILE = "submissions.xlsx"

def append_to_excel(data_dict):
    df = pd.DataFrame([data_dict])

    if not os.path.exists(EXCEL_FILE):
        df.to_excel(EXCEL_FILE, index=False)
    else:
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            existing_df = pd.read_excel(EXCEL_FILE)
            df.to_excel(writer, index=False, header=False, startrow=len(existing_df))

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  # UI page for users

@app.route("/parse-form", methods=["POST"])
def parse_form():
    try:
        data = request.get_json()
        user_prompt = data.get("prompt", "").strip()
        full_prompt = f"{system_prompt}\n\nUser Input:\n{user_prompt}"

        response = co.generate(
            model='command-r-plus',
            prompt=full_prompt,
            max_tokens=300,
            temperature=0.2
        )

        result_text = response.generations[0].text.strip()
        lines = [line for line in result_text.split("\n") if ":" in line]
        result_dict = {}

        for line in lines:
            key, val = line.split(":", 1)
            result_dict[key.strip()] = val.strip()

        # Save to Excel
        append_to_excel(result_dict)

        return jsonify({
            "status": "success",
            "result": result_text
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Endpoint for organizer to download Excel file
@app.route("/download-excel", methods=["GET"])
def download_excel():
    if os.path.exists(EXCEL_FILE):
        return send_file(EXCEL_FILE, as_attachment=True)
    else:
        return "No submissions yet.", 404

if __name__ == "__main__":
    app.run(debug=True)
