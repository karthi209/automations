import subprocess
import json
import sys
import time
import os

# Constants
TOOL_VERSION_CONFIG = '/tmp/test_tools/tool_version_config.json'
OUTPUT_FILE = '/tmp/test_tools/tool_versions.json'
IMAGE_METADATA_FILE = '/tmp/test_tools/image_metadata.json'
PREV_IMAGE_METADATA = "prev_image_metadata.json"
TEMP_DIR = "/tmp/test_tools"

def safe_subprocess_call(command, description):
    """Executes a subprocess command and logs errors if it fails."""
    try:
        print(f"🔹 Running: {description}...")
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        sys.exit(1)

def run_docker_tests(image_name):
    container_name = f"test-container-{int(time.time())}"
    host_tool_version_output = os.path.abspath("./tool_versions.json")
    host_image_metadata_output = os.path.abspath("./image_metadata.json")

    # Check if the image exists locally
    check_cmd = ["docker", "images", "-q", image_name]
    result = subprocess.run(check_cmd, capture_output=True, text=True)
    if not result.stdout.strip():
        print(f"⚠️ Image '{image_name}' not found locally, pulling from remote...")
        safe_subprocess_call(["docker", "pull", image_name], "pull Docker image")

    # Start the container in detached mode
    safe_subprocess_call(["docker", "run", "-d", "--user", "runner", "--name", container_name, image_name, "tail", "-f", "/dev/null"], "start Docker container")

    # Ensure /tmp/test_tools directory exists inside the container
    safe_subprocess_call(["docker", "exec", container_name, "mkdir", "-p", TEMP_DIR], "prepare /tmp/test_tools directory")
    safe_subprocess_call(["docker", "exec", container_name, "chmod", "777", TEMP_DIR], "set permissions for /tmp/test_tools directory")

    # Copy tool version config file into the container
    safe_subprocess_call(["docker", "cp", "./tool_version_config.json", f"{container_name}:{TEMP_DIR}/tool_version_config.json"], "copy tool_version_config.json")

    # Retrieve image metadata
    print("🔍 Collecting image metadata...")
    metadata_script = """
import json, subprocess

TEMP_DIR = "/tmp/test_tools"
IMAGE_METADATA_FILE = f"{TEMP_DIR}/image_metadata.json"

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
    "Layer Count": run_command("docker history --no-trunc $(hostname) | wc -l"),
    "Image Size": run_command("du -sh / | cut -f1"),
}

with open(IMAGE_METADATA_FILE, 'w') as f:
    json.dump(metadata, f, indent=4)

print("✅ Image metadata collected!")
"""
    safe_subprocess_call(["docker", "exec", container_name, "python3", "-c", metadata_script], "retrieve image metadata")

    # Retrieve installed package list
    safe_subprocess_call(["docker", "exec", container_name, "rpm", "-qa", "|", "sort", ">", f"{TEMP_DIR}/installed_packages.txt"], "retrieve installed packages")

    # Run tool version checks
    print("🔍 Running tool version checks...")
    tool_check_script = """
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
    safe_subprocess_call(["docker", "exec", container_name, "python3", "-c", tool_check_script], "execute tool version retrieval inside container")

    # Copy results back to host
    safe_subprocess_call(["docker", "cp", f"{container_name}:{TEMP_DIR}/tool_versions.json", host_tool_version_output], "copy tool versions output")
    safe_subprocess_call(["docker", "cp", f"{container_name}:{TEMP_DIR}/image_metadata.json", host_image_metadata_output], "copy image metadata output")

    print(f"📁 Tool versions saved at: {host_tool_version_output}")
    print(f"📁 Image metadata saved at: {host_image_metadata_output}")

    # Stop and remove container
    safe_subprocess_call(["docker", "stop", container_name], "stop container")
    safe_subprocess_call(["docker", "rm", container_name], "remove container")

    # Compare metadata with previous release (if exists)
    if os.path.exists(PREV_IMAGE_METADATA):
        print("🔍 Comparing with previous image metadata...")
        with open(PREV_IMAGE_METADATA, 'r') as f1, open(host_image_metadata_output, 'r') as f2:
            prev_meta = json.load(f1)
            curr_meta = json.load(f2)
        
        changes = {k: (prev_meta[k], curr_meta[k]) for k in prev_meta if prev_meta[k] != curr_meta[k]}
        if changes:
            print("⚠️ Changes detected:")
            for key, (old, new) in changes.items():
                print(f"🔹 {key}: {old} → {new}")
        else:
            print("✅ No changes detected in image metadata.")
    else:
        print("⚠️ No previous image metadata found for comparison.")

    # Save current metadata for next comparison
    os.rename(host_image_metadata_output, PREV_IMAGE_METADATA)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python test_manager.py <docker_image_name>")
        sys.exit(1)

    docker_image_name = sys.argv[1]
    run_docker_tests(docker_image_name)
