from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify
import anthropic
import os

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    pregunta = data.get("message", "")

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1000,
        system="Eres un experto en Salesforce Marketing Cloud. Respondes de forma clara y concisa en español. Usas ejemplos prácticos cuando es útil.",
        messages=[
            {"role": "user", "content": pregunta}
        ]
    )

    return jsonify({"response": message.content[0].text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)