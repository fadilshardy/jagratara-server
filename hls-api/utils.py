import os
import shutil
import subprocess
from werkzeug.utils import secure_filename



def run_ffmpeg(input_path, output_path):
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
      output_path ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    
    return process

def save_uploaded_file(file, upload_dir):
    """Save the uploaded file to the specified directory."""
    if file.filename == '':
        raise ValueError("No file selected")
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)
    return file_path

def remove_file(file_path):
    """Remove a file if it exists."""
    if os.path.exists(file_path):
        os.remove(file_path)

def clear_output_dir(output_dir):
    for f in os.listdir(output_dir):
        file_path = os.path.join(output_dir, f)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error cleaning output dir: {e}")
