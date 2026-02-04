"""
Silver Tier – MCP Server
External actions handler (email, LinkedIn, etc.)
"""

from flask import Flask, request, jsonify
from linkedin_post import post_to_linkedin

app = Flask(__name__)

@app.route("/linkedin", methods=["POST"])
def linkedin():
    data = request.json
    post_to_linkedin(data["text"])
    return jsonify({"status": "posted"})

@app.route("/send_email", methods=["POST"])
def send_email():
    data = request.json
    print("📧 Email sent to:", data["to"])
    return jsonify({"status": "sent"})

if __name__ == "__main__":
    app.run(port=3333)

