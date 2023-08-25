import subprocess
import json
import os

import cv2


def upload_helper(video_params):
    command = ['node', 'upload_script.js']
    if(not is_vertical_aspect_ratio(video_params['file'])):
        print("Video is horizontal, skipped upload")
        return
    # Pass the video_params as JSON string through command-line arguments
    command.extend([json.dumps(video_params)])
    # Run the command and capture the output
    output = subprocess.run(command, capture_output=True, text=True, env=os.environ)

    # Get the exit code of the command
    exit_code = output.returncode

    if exit_code != 0:
        # Command returned a non-zero exit status
        error_message = output.stderr
        print(f"Command execution failed with error:\n{error_message}")
    else:
        print(f"Successfully uploaded video: \n{output.stdout}")



def is_vertical_aspect_ratio(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get the width and height of the video frames
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"{width}x{height}")
    # Calculate the aspect ratio
    aspect_ratio = width / height

    # Close the video file
    cap.release()

    return height>=width

# Provide the path to your video file
video_path = 'path/to/your/video/file.mp4'
