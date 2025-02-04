import subprocess
import json
import time
import os

# Constants for file paths
TOOL_VERSION_CONFIG = 'tool_version_config.json'
OUTPUT_FILE = 'output.json'  # Tool version output file inside the container
CONTAINER_TMP_DIR = "/tmp/test_tools"  # Working directory inside the container

# Host-side file paths
HOST_CONFIG_FILE = os.path.abspath("./tool_version_config.json")  # Tool version config
HOST_TOOL_VERSION_OUTPUT = os.path.abspath("./tool_versions.json")  # Tool version output

# Function to execute shell commands safely
def safe_subprocess_call(command, description):
    try:
        print(f"Running: {description}...")
        subprocess.check_call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"Error during {description}: {e}")

# Function to extract the version of a tool using the command from the config
def get_version(tool, command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            return version if version else "0.0.0"
        else:
            return f"{tool}: Error executing command"
    except Exception as e:
        return f"{tool}: {str(e)}"

# Function to execute tool version extraction inside the container
def run_tool_version_check_inside_container(container_name):
    tool_versions = {}

    # Load the tool version config
    try:
        with open(TOOL_VERSION_CONFIG, 'r') as f:
            tools_config = json.load(f)

        for tool, details in tools_config.items():
            command = details.get('command', '')
            tool_versions[tool] = get_version(tool, command) if command else f"{tool}: No command found in config"
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        return

    # Save results inside the container
    with open(OUTPUT_FILE, 'w') as outfile:
        json.dump(tool_versions, outfile, indent=4)

    # Copy results back to host
    safe_subprocess_call(["docker", "cp", f"{container_name}:{CONTAINER_TMP_DIR}/output.json", HOST_TOOL_VERSION_OUTPUT],
                         "retrieve tool version output from container")

    print(f"Tool versions saved to {HOST_TOOL_VERSION_OUTPUT}")

# Function to run the entire process inside a Docker container
def run_docker_tool_check(image_name):
    container_name = f"test-container-{int(time.time())}"

    # Check if the image is available locally
    check_cmd = ["docker", "images", "-q", image_name]
    result = subprocess.run(check_cmd, capture_output=True, text=True)

    if not result.stdout.strip():
        print(f"Image '{image_name}' not found locally. Pulling from remote...")
        safe_subprocess_call(["docker", "pull", image_name], "pull Docker image")
    else:
        print(f"Image '{image_name}' found locally.")

    # Run the container
    safe_subprocess_call(["docker", "run", "-d", "--name", container_name, image_name, "tail", "-f", "/dev/null"],
                         "start Docker container")

    # Create directory inside container
    safe_subprocess_call(["docker", "exec", container_name, "mkdir", "-p", CONTAINER_TMP_DIR],
                         "create working directory in container")

    # Copy tool version config file into container
    safe_subprocess_call(["docker", "cp", HOST_CONFIG_FILE, f"{container_name}:{CONTAINER_TMP_DIR}/tool_version_config.json"],
                         "copy tool_version_config.json")

    # Execute tool version checking inside the container
    run_tool_version_check_inside_container(container_name)

    # Stop and remove the container
    safe_subprocess_call(["docker", "stop", container_name], "stop container")
    safe_subprocess_call(["docker", "rm", container_name], "remove container")

if __name__ == '__main__':
    docker_image = "your-docker-image"  # Replace with the actual image name
    run_docker_tool_check(docker_image)
