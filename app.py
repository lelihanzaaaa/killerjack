from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Enable CORS if needed

# Define CSV file name
file_name = "data.csv"

@app.route("/")
def index():
    return render_template("index.html")  # Serve HTML file

@app.route("/submit", methods=["POST"])
def save_to_csv():
    try:
        data = request.json  

        # Validate data fields
        if not all(k in data for k in ("name", "age", "salary", "position")):
            return jsonify({"error": "Missing fields"}), 400

        # Convert to DataFrame
        new_entry = pd.DataFrame([data])

        # Check if file exists and append data correctly
        if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
            df = pd.read_csv(file_name, encoding="utf-8")
            df = pd.concat([df, new_entry], ignore_index=True)
        else:
            df = new_entry  # First-time creation

        # Save data to CSV (without extra index column)
        df.to_csv(file_name, index=False, encoding="utf-8")

        return jsonify({"message": "Data saved successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
