import subprocess
import json
import os

def upload_helper(video_params):
    command = ['node', 'upload_script.js']

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
