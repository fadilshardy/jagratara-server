from flask import jsonify, request
import os
from utils import save_uploaded_file, remove_file, clear_output_dir, run_ffmpeg
from config import SHARED_FOLDER, OUTPUT_DIR

def setup_routes(app):
    @app.route("/list_videos", methods=["GET"])
    def list_videos():
        videos = [f for f in os.listdir(SHARED_FOLDER) if f.endswith((".mp4", ".mov", ".mkv"))]
        return jsonify({"videos": videos})

    @app.route("/hello", methods=["GET"])
    def hello_world():
        return jsonify({"message": "Hello, World!"})

    # @app.route("/generate_hls", methods=["POST"])
    # def generate_hls():
    #     if 'file' not in request.files:
    #         return jsonify({"error": "No file provided"}), 400

    #     file = request.files['file']
    #     try:
    #         input_path = save_uploaded_file(file, SHARED_FOLDER)
    #         output_path = os.path.join(OUTPUT_DIR, "output.m3u8")
    #         clear_output_dir(OUTPUT_DIR)

    #         run_ffmpeg(input_path, output_path)
    #         remove_file(input_path)

    #         return jsonify({
    #             "status": "success",
    #             "playlist_url": f"{request.host_url}hls/output.m3u8"
    #         })

    #     except ValueError as e:
    #         return jsonify({"error": str(e)}), 400
    #     except Exception as e:
    #         return jsonify({"error": str(e)}), 500

    @app.route("/generate_hls", methods=["POST"])
    def generate_hls():
        data = request.get_json()
        video_name = data.get("video_name", None)
        if not video_name:
            return jsonify({"error": "video_name is required"}), 400
        
        input_path = os.path.join(SHARED_FOLDER, video_name)
        output_path = os.path.join(OUTPUT_DIR, "output.m3u8")
 
        clear_output_dir(OUTPUT_DIR)

        run_ffmpeg(input_path, output_path)

        return jsonify({
            "status": "success",
            "playlist_url": f"{request.host_url}hls/output.m3u8"
        })