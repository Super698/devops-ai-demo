import os
from flask import Flask, render_template_string, request
from google import genai

app = Flask(__name__)

# Initialize the Gemini client using the environment variable
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


@app.route("/", methods=["GET", "POST"])
def home():
  ai_response = ""
  if request.method == "POST":
    user_prompt = request.form.get("prompt")
    try:
      # Updated model name to gemini-2.0-flash
      response = client.models.generate_content(
          model="gemini-3.8-flash",
          contents=user_prompt,
      )
      ai_response = response.text
    except Exception as e:
      ai_response = f"Error connecting to AI: {str(e)}"

  return render_template_string("""
        <!doctype html>
        <html lang="en">
        <head>
            <title>Gemini-Powered DevOps App</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 50px; background: #f4f4f9; color: #333; }
                .container { max-width: 600px; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
                textarea { width: 100%; height: 100px; padding: 10px; margin-bottom: 10px; border-radius: 4px; border: 1px solid #ccc; }
                button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
                button:hover { background: #0056b3; }
                .result { margin-top: 20px; padding: 15px; background: #e9ecef; border-left: 4px solid #007bff; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Gemini-Powered DevOps Flask App</h2>
                <form method="POST">
                    <label>Ask or prompt the AI:</label><br>
                    <textarea name="prompt" placeholder="Type something here...">{{ request.form.get('prompt', '') }}</textarea><br>
                    <button type="submit">Generate AI Response</button>
                </form>
                {% if ai_response %}
                    <div class="result">
                        <strong>AI Output:</strong>
                        <p>{{ ai_response }}</p>
                    </div>
                {% endif %}
            </div>
        </body>
        </html>
    """, ai_response=ai_response)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5001)