from flask import Flask, jsonify, request
from flask_cors import CORS
import shutil
from werkzeug.utils import secure_filename

import os, subprocess
import threading

app = Flask(__name__)
CORS(app)

SHARED_FOLDER = "/shared"
OUTPUT_DIR = "/hls"

@app.route("/list_videos", methods=["GET"])
def list_videos():
    videos = [f for f in os.listdir(SHARED_FOLDER) if f.endswith((".mp4", ".mov"))]
    return jsonify({"videos": videos})

@app.route("/hello", methods=["GET"])
def hello_world():
    return jsonify({"message": "Hello, World!"})

def run_ffmpeg(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

@app.route("/generate_hls", methods=["POST"])
def generate_hls():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        filename = secure_filename(file.filename)
        input_path = os.path.join(SHARED_FOLDER, filename)
        file.save(input_path)

        output_path = os.path.join(OUTPUT_DIR, "output.m3u8")

        def clear_output_dir():
            for f in os.listdir(OUTPUT_DIR):
                file_path = os.path.join(OUTPUT_DIR, f)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Error cleaning output dir: {e}")

        clear_output_dir()

        command = [
            "ffmpeg", "-y", "-i", input_path,
            "-c:v", "copy", "-c:a", "copy",
            "-f", "hls",
            "-hls_time", "60",
            "-hls_playlist_type", "event",
            "-hls_flags", "independent_segments+temp_file",
            "-hls_segment_type", "fmp4",
            "-hls_fmp4_init_filename", "video_init.mp4",
            "-hls_list_size", "3",
            output_path
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()  # Wait for the process to complete

        os.remove(input_path)
        return jsonify({
            "status": "success",
            "playlist_url": f"{request.host_url}hls/output.m3u8"
        })

    except Exception as e:
        if os.path.exists(input_path):
            os.remove(input_path)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


