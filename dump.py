import subprocess
import sys

def safe_subprocess_call(command, description):
    """Executes a subprocess command and logs errors if it fails."""
    try:
        print(f"🔹 Running: {description}...")
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        sys.exit(1)



import json
import subprocess
import time
from .subprocess_utils import safe_subprocess_call
from .metadata_utils import save_metadata

TEMP_DIR = "/tmp/test_tools"

def get_image_metadata(image_name):
    """Retrieve metadata of the Docker image."""
    print("🔍 Retrieving Docker image metadata...")

    # Get image details using `docker inspect`
    inspect_cmd = f"docker inspect {image_name}"
    result = subprocess.run(inspect_cmd, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Failed to inspect image {image_name}: {result.stderr}")
        sys.exit(1)

    image_info = json.loads(result.stdout)[0]  # Get first (and only) result

    # Get image size in MB
    size_cmd = f"docker images --format '{{{{.Size}}}}' {image_name}"
    size_result = subprocess.run(size_cmd, shell=True, capture_output=True, text=True)

    metadata = {
        "Image_ID": image_info["Id"],
        "Repo_Tags": image_info.get("RepoTags", []),
        "Created": image_info["Created"],
        "Size": size_result.stdout.strip(),
        "Architecture": image_info.get("Architecture", "unknown"),
        "OS": image_info.get("Os", "unknown"),
        "Digest": image_info.get("RepoDigests", [])
    }

    # Save metadata to file
    save_metadata(image_name, metadata)
    return metadata

def run_docker_tests(image_name):
    timestamp = int(time.time())
    container_name = f"test-container-{timestamp}"

    # Ensure the image exists locally
    check_cmd = f"docker images -q {image_name}"
    result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        print(f"⚠️ Image '{image_name}' not found locally, pulling from remote...")
        safe_subprocess_call(f"docker pull {image_name}", "pull Docker image")

    # Retrieve and save image metadata
    get_image_metadata(image_name)

    # Start the container and perform tests...






import json
import os

def save_metadata(image_name, metadata):
    """Save metadata to a file."""
    metadata_file = f"./image_metadata_{image_name.replace(':', '_').replace('/', '_')}.json"
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"📁 Image metadata saved at: {metadata_file}")






import json
import subprocess
import shutil

TOOL_VERSION_CONFIG = '/tmp/test_tools/tool_version_config.json'
OUTPUT_FILE = '/tmp/test_tools/tool_versions.json'

def get_version(tool, command):
    if not shutil.which(tool.split()[0]):  # Handle cases like "python3" vs "python"
        return "Not installed"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip() or result.stderr.strip()  # Some tools output version to stderr
        return "Error running version check"
    except Exception as e:
        return str(e)

def get_tool_versions():
    tool_versions = {}
    try:
        with open(TOOL_VERSION_CONFIG, 'r') as f:
            tools_config = json.load(f)
        
        # Add version info for each configured tool
        for tool, details in tools_config.items():
            command = details.get('command', '')
            tool_versions[tool] = get_version(tool, command) if command else "No command found"
        
    except Exception as e:
        print(f"Error: {str(e)}")
        tool_versions["error"] = str(e)
    
    # Write results
    with open(OUTPUT_FILE, 'w') as outfile:
        json.dump(tool_versions, outfile, indent=2, sort_keys=True)

get_tool_versions()





#!/bin/bash
if command -v rpm > /dev/null; then
    rpm -qa | sort > /tmp/test_tools/packages.txt
elif command -v dpkg > /dev/null; then
    dpkg -l | awk '/^ii/ {print $2 "=" $3}' | sort > /tmp/test_tools/packages.txt
elif command -v apk > /dev/null; then
    apk info -v | sort > /tmp/test_tools/packages.txt
else
    echo "No supported package manager found" > /tmp/test_tools/packages.txt
fi




import sys
from utils.docker_utils import run_docker_tests

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python test_manager.py <docker_image_name>")
        sys.exit(1)

    docker_image_name = sys.argv[1]
    run_docker_tests(docker_image_name)
