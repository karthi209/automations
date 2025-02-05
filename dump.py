import subprocess
import json
import sys
import time
import os

# Constants
TOOL_VERSION_CONFIG = '/tmp/test_tools/tool_version_config.json'
OUTPUT_FILE = '/tmp/test_tools/tool_versions.json'

def safe_subprocess_call(command, description):
    """Executes a subprocess command and logs errors if it fails."""
    try:
        print(f"Running: {description}...")
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        print(f"Error during {description}: {e}")
        sys.exit(1)

def run_docker_tests(image_name):
    container_name = f"test-container-{int(time.time())}"
    container_tmp_dir = "/tmp/test_tools"
    host_config_file = os.path.abspath("./tool_version_config.json")
    host_tool_version_output = os.path.abspath("./tool_versions.json")

    # Check if the image exists locally, if not, pull it
    check_cmd = ["docker", "images", "-q", image_name]
    result = subprocess.run(check_cmd, capture_output=True, text=True)
    
    if not result.stdout.strip():
        print(f"Image '{image_name}' not found locally, pulling from remote...")
        safe_subprocess_call(["docker", "pull", image_name], "pull Docker image")
        
    # Inspect the docker image
    safe_subprocess_call(["docker", "run", "-d", "--user", "runner", "--name", container_name, image_name, "tail", "-f", "/dev/null"], "start Docker container")

    # Start the container in detached mode
    safe_subprocess_call(["docker", "run", "-d", "--user", "runner", "--name", container_name, image_name, "tail", "-f", "/dev/null"], "start Docker container")

    # Ensure /tmp/test_tools directory exists inside the container
    safe_subprocess_call(["docker", "exec", container_name, "mkdir", "-p", container_tmp_dir], "prepare /tmp/test_tools directory")
    safe_subprocess_call(["docker", "exec", container_name, "chmod", "777", container_tmp_dir], "set permissions for /tmp/test_tools directory")

    # Copy test scripts and tool_version_config.json to /tmp folder inside the container
    safe_subprocess_call(["docker", "cp", host_config_file, f"{container_name}:{container_tmp_dir}/tool_version_config.json"], "copy tool_version_config.json")

    # Verify the copied files
    safe_subprocess_call(["docker", "exec", container_name, "ls", "-la", container_tmp_dir], "list contents of /tmp/test_tools")

    # Run tool version retrieval inside the container
    safe_subprocess_call([
        "docker", "exec", container_name, "python3", "-c", """
import json, subprocess

TOOL_VERSION_CONFIG = '/tmp/test_tools/tool_version_config.json'
OUTPUT_FILE = '/tmp/test_tools/tool_versions.json'

def get_version(tool, command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else "0.0.0"
    except Exception as e:
        return str(e)

def get_tool_versions():
    tool_versions = {}
    try:
        with open(TOOL_VERSION_CONFIG, 'r') as f:
            tools_config = json.load(f)
        for tool, details in tools_config.items():
            command = details.get('command', '')
            tool_versions[tool] = get_version(tool, command) if command else "No command found"
    except Exception as e:
        print(f"Error: {str(e)}")
    with open(OUTPUT_FILE, 'w') as outfile:
        json.dump(tool_versions, outfile, indent=4)

get_tool_versions()
"""
    ], "execute tool version retrieval inside container")

    # Copy the tool versions output file back to the host
    safe_subprocess_call(["docker", "cp", f"{container_name}:{container_tmp_dir}/tool_versions.json", host_tool_version_output], "copy tool versions output")

    print(f"Tool versions saved at {host_tool_version_output}")

    # Stop and remove the container
    safe_subprocess_call(["docker", "stop", container_name], "stop container")
    safe_subprocess_call(["docker", "rm", container_name], "remove container")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python test_manager.py <docker_image_name>")
        sys.exit(1)

    docker_image_name = sys.argv[1]
    run_docker_tests(docker_image_name)
