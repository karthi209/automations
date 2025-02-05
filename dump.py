# test_manager.py

import sys
import time
from docker_helper import get_image_metadata, run_docker_container, cleanup_container
from utils import safe_subprocess_call

TEMP_DIR = "/tmp/test_tools"

def run_docker_tests(image_name):
    # Generate a unique container name
    container_name = run_docker_container(image_name)

    # Ensure /tmp/test_tools exists in the container
    safe_subprocess_call(f"docker exec {container_name} mkdir -p {TEMP_DIR}", "prepare /tmp/test_tools directory")
    safe_subprocess_call(f"docker exec {container_name} chmod 755 {TEMP_DIR}", "set permissions for /tmp/test_tools directory")

    # Copy tool version config file into the container
    safe_subprocess_call(
        f"docker cp ./tool_version_config.json {container_name}:{TEMP_DIR}/tool_version_config.json",
        "copy tool_version_config.json"
    )

    # Run tool version checks inside the container
    print("🔍 Running tool version checks...")
    tool_check_script = open('tool_version_check.py', 'r').read()
    safe_subprocess_call(
        f"docker exec {container_name} python3 -c '{tool_check_script}'",
        "execute tool version retrieval inside container"
    )

    # Get installed packages
    package_script = open('package_check.sh', 'r').read()
    safe_subprocess_call(
        f"docker exec {container_name} bash -c '{package_script}'",
        "retrieve installed packages"
    )

    # Copy results back to host
    host_tool_version_output = f"./tool_versions_{image_name.replace(':', '_').replace('/', '_')}.json"
    host_packages_output = f"./packages_{image_name.replace(':', '_').replace('/', '_')}.txt"
    safe_subprocess_call(
        f"docker cp {container_name}:{TEMP_DIR}/tool_versions.json {host_tool_version_output}",
        "copy tool versions output"
    )
    safe_subprocess_call(
        f"docker cp {container_name}:{TEMP_DIR}/packages.txt {host_packages_output}",
        "copy packages list"
    )

    # Retrieve and save image metadata
    metadata_file = get_image_metadata(image_name)

    print(f"📁 Tool versions saved at: {host_tool_version_output}")
    print(f"📁 Packages list saved at: {host_packages_output}")
    print(f"📁 Docker image metadata saved at: {metadata_file}")

    cleanup_container(container_name)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python test_manager.py <docker_image_name>")
        sys.exit(1)

    docker_image_name = sys.argv[1]
    run_docker_tests(docker_image_name)





# package_check.sh

if command -v rpm > /dev/null; then
    rpm -qa | sort > /tmp/test_tools/packages.txt
elif command -v dpkg > /dev/null; then
    dpkg -l | awk '/^ii/ {print $2 "=" $3}' | sort > /tmp/test_tools/packages.txt
elif command -v apk > /dev/null; then
    apk info -v | sort > /tmp/test_tools/packages.txt
else
    echo "No supported package manager found" > /tmp/test_tools/packages.txt
fi




# tool_version_check.py

import json
import subprocess
import shutil
from pathlib import Path

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




# docker_helper.py

import subprocess
import json
import os
from utils import safe_subprocess_call, run_subprocess

TEMP_DIR = "/tmp/test_tools"

def get_image_metadata(image_name):
    """Retrieve metadata of the Docker image."""
    print("🔍 Retrieving Docker image metadata...")

    # Get image details using `docker inspect`
    inspect_cmd = f"docker inspect {image_name}"
    result = run_subprocess(inspect_cmd)

    if result.returncode != 0:
        print(f"❌ Failed to inspect image {image_name}: {result.stderr}")
        sys.exit(1)

    image_info = json.loads(result.stdout)[0]  # Get first (and only) result

    # Get image size in MB
    size_cmd = f"docker images --format '{{{{.Size}}}}' {image_name}"
    size_result = run_subprocess(size_cmd)

    # Extract relevant details
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
    metadata_file = f"./image_metadata_{image_name.replace(':', '_').replace('/', '_')}.json"
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"📁 Image metadata saved at: {metadata_file}")
    return metadata_file

def run_docker_container(image_name):
    """Start a Docker container."""
    timestamp = int(time.time())
    container_name = f"test-container-{timestamp}"
    safe_subprocess_call(
        f"docker run -d --user runner --name {container_name} {image_name} tail -f /dev/null",
        "start Docker container"
    )
    return container_name

def cleanup_container(container_name):
    """Stop and remove Docker container."""
    try:
        safe_subprocess_call(f"docker stop {container_name}", "stop container")
        safe_subprocess_call(f"docker rm {container_name}", "remove container")
    except subprocess.CalledProcessError:
        print(f"⚠️ Warning: Failed to cleanup container {container_name}")



# utils.py

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

def run_subprocess(command):
    """Runs a subprocess command and returns the result."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result
