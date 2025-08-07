from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid
import base64

app = Flask(__name__)

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing YouTube URL"}), 400

    # Prepare cookies
    cookies_b64 = os.getenv("YOUTUBE_COOKIES")
    cookies_path = "/tmp/cookies.txt"
    if cookies_b64:
        try:
            with open(cookies_path, "wb") as f:
                f.write(base64.b64decode(cookies_b64))
        except Exception as e:
            return jsonify({"error": f"Failed to decode cookies: {str(e)}"}), 500
    else:
        cookies_path = None  # no cookies

    # Prepare filename and yt-dlp options
    filename = f"/tmp/{uuid.uuid4().hex}.mp4"
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': filename,
        'quiet': True,
        'merge_output_format': 'mp4',
        'noplaylist': True
    }

    if cookies_path:
        ydl_opts['cookiefile'] = cookies_path

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
