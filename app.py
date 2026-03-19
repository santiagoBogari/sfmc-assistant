from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify
import anthropic
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

        data = request.get_json()
        pregunta = data.get("message", "")

        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1000,
            system="You are an expert in Salesforce Marketing Cloud. You respond clearly and concisely in English. You use practical examples when helpful.",
            messages=[
                {"role": "user", "content": pregunta}
            ]
        )

        return jsonify({"response": message.content[0].text})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
    