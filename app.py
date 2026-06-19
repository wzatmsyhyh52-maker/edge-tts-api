from flask import Flask, request, jsonify
import asyncio
import edge_tts
import os
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "running"}

@app.route("/tts", methods=["GET"])
def tts():
    text = request.args.get("text")

    if not text:
        return jsonify({"error": "text parameter required"}), 400

    filename = f"{uuid.uuid4()}.mp3"

    async def generate():
        communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
        await communicate.save(filename)

    asyncio.run(generate())

    return jsonify({
        "success": True,
        "file": filename
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
