from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
import requests

app = Flask(__name__)

genai.configure(api_key="AIzaSyAVEhfxVMFAOBQMVszjhBGb9V6zZES81f4")
model = genai.GenerativeModel("models/gemini-1.5-flash")
history = []

def get_latest_ipl_winner():
    try:
        url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
        headers = {
            "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",
            "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers).json()
        for match in response["typeMatches"]:
            if match["matchType"] == "League" and "ipl" in match["seriesMatches"][0]["seriesAdWrapper"]["seriesName"].lower():
                last_match = match["seriesMatches"][0]["seriesAdWrapper"]["matches"][-1]
                return f"🏆 Latest IPL Winner: {last_match['matchInfo']['team1']['teamName']} vs {last_match['matchInfo']['team2']['teamName']} – Result: {last_match['matchInfo']['status']}"
    except:
        return "⚠️ Couldn't fetch IPL info right now."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_text = data.get("message", "")

    if "ipl" in user_text.lower() and "winner" in user_text.lower():
        reply = get_latest_ipl_winner()
    else:
        history.append({"role": "user", "parts": [user_text]})
        response = model.generate_content(history)
        history.append({"role": "model", "parts": [response.text]})
        reply = response.text

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
