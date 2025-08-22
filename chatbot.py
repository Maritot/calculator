import google.generativeai as genai
import requests

# 🔑 Set your Gemini API Key
genai.configure(api_key="AIzaSyAVEhfxVMFAOBQMVszjhBGb9V6zZES81f4")

model = genai.GenerativeModel("models/gemini-1.5-flash")

history = []  # 🔹 Chat memory

# 🔹 Function to get latest IPL winner using Cricbuzz unofficial API
def get_latest_ipl_winner():
    try:
        url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
        headers = {
            "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",  # Get free key from RapidAPI
            "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers).json()
        for match in response["typeMatches"]:
            if match["matchType"] == "League" and "ipl" in match["seriesMatches"][0]["seriesAdWrapper"]["seriesName"].lower():
                last_match = match["seriesMatches"][0]["seriesAdWrapper"]["matches"][-1]
                return f"🏆 Latest IPL Winner: {last_match['matchInfo']['team1']['teamName']} vs {last_match['matchInfo']['team2']['teamName']} – Result: {last_match['matchInfo']['status']}"
    except:
        return "⚠️ Couldn't fetch IPL info right now."

def chat_with_gemini(prompt):
    # If question is about IPL winner → use API
    if "ipl" in prompt.lower() and "winner" in prompt.lower():
        return get_latest_ipl_winner()

    history.append({"role": "user", "parts": [prompt]})
    response = model.generate_content(history)
    history.append({"role": "model", "parts": [response.text]})
    return response.text

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        print("Bot:", chat_with_gemini(user_input))
