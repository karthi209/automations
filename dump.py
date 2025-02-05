import subprocess
import json
import sys
import time
import os

# Constants
TEMP_DIR = "/tmp/test_tools"
TOOL_VERSION_CONFIG = f"{TEMP_DIR}/tool_version_config.json"
OUTPUT_FILE_TEMPLATE = f"{TEMP_DIR}/tool_versions_{{}}.json"
IMAGE_METADATA_FILE_TEMPLATE = f"{TEMP_DIR}/image_metadata_{{}}.json"

def safe_subprocess_call(command, description):
    """Executes a subprocess command and logs errors if it fails."""
    try:
        print(f"🔹 Running: {description}...")
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        sys.exit(1)

def run_docker_tests(image_name):
    timestamp = int(time.time())
    output_file = OUTPUT_FILE_TEMPLATE.format(image_name.replace(':', '_'))
    image_metadata_file = IMAGE_METADATA_FILE_TEMPLATE.format(image_name.replace(':', '_'))
    container_name = f"test-container-{timestamp}"

    # Check if the image exists locally
    result = subprocess.run(["docker", "images", "-q", image_name], capture_output=True, text=True)
    if not result.stdout.strip():
        print(f"⚠️ Image '{image_name}' not found locally, pulling from remote...")
        safe_subprocess_call(["docker", "pull", image_name], "pull Docker image")

    # Start the container in detached mode
    safe_subprocess_call([
        "docker", "run", "-d", "--user", "runner", "--name", container_name, image_name, "tail", "-f", "/dev/null"
    ], "start Docker container")

    # Prepare container environment
    safe_subprocess_call(["docker", "exec", container_name, "mkdir", "-p", TEMP_DIR], "prepare /tmp/test_tools directory")
    safe_subprocess_call(["docker", "cp", "./tool_version_config.json", f"{container_name}:{TOOL_VERSION_CONFIG}"], "copy tool_version_config.json")

    # Retrieve installed tools' versions
    print("🔍 Running tool version checks...")
    tool_check_script = f"""
import json, subprocess
TOOL_VERSION_CONFIG = '{TOOL_VERSION_CONFIG}'
OUTPUT_FILE = '{output_file}'

def get_version(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else "Not Found"
    except:
        return "Error"

def get_tool_versions():
    tool_versions = {}
    try:
        with open(TOOL_VERSION_CONFIG, 'r') as f:
            tools_config = json.load(f)
        for tool, details in tools_config.items():
            command = details.get('command', '')
            tool_versions[tool] = get_version(command) if command else "No command found"
    except Exception as e:
        tool_versions['error'] = str(e)
    with open(OUTPUT_FILE, 'w') as outfile:
        json.dump(tool_versions, outfile, indent=4)
get_tool_versions()
"""
    safe_subprocess_call(["docker", "exec", container_name, "python3", "-c", tool_check_script], "execute tool version retrieval inside container")

    # Retrieve image metadata
    print("🔍 Collecting image metadata...")
    metadata_script = f"""
import json, subprocess
TEMP_DIR = '{TEMP_DIR}'
IMAGE_METADATA_FILE = '{image_metadata_file}'

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else "N/A"
    except:
        return "Error"

metadata = {
    "Base Image": run_command("cat /etc/os-release"),
    "Kernel Version": run_command("uname -r"),
    "Default User": run_command("whoami"),
    "Installed Packages": run_command("rpm -qa | sort")
}

with open(IMAGE_METADATA_FILE, 'w') as f:
    json.dump(metadata, f, indent=4)
print("✅ Image metadata collected!")
"""
    safe_subprocess_call(["docker", "exec", container_name, "python3", "-c", metadata_script], "retrieve image metadata")

    # Copy results back to host
    safe_subprocess_call(["docker", "cp", f"{container_name}:{output_file}", output_file], "copy tool versions output")
    safe_subprocess_call(["docker", "cp", f"{container_name}:{image_metadata_file}", image_metadata_file], "copy image metadata output")

    print(f"📁 Tool versions saved at: {output_file}")
    print(f"📁 Image metadata saved at: {image_metadata_file}")

    # Stop and remove container
    safe_subprocess_call(["docker", "stop", container_name], "stop container")
    safe_subprocess_call(["docker", "rm", container_name], "remove container")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python test_manager.py <docker_image_name>")
        sys.exit(1)
    run_docker_tests(sys.argv[1])
