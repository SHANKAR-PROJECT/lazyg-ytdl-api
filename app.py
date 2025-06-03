from flask import Flask, request, send_file, jsonify
from pytube import YouTube
import os
import uuid

app = Flask(__name__)

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing YouTube URL"}), 400

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        filename = f"/tmp/{uuid.uuid4().hex}.mp4"
        stream.download(filename=filename)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
