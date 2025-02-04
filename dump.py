import subprocess
import json
import sys
import time
import os

# Path to the tool version config file
TOOL_VERSION_CONFIG = '/tmp/test_tools/tool_version_config.json'
OUTPUT_FILE = '/tmp/test_tools/tool_versions.json'  # Output file location inside the container

# Function to extract the version of a tool using the command from the config
def get_version(tool, command):
    try:
        # Execute the command and capture the output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Check if the command ran successfully
        if result.returncode == 0:
            version = result.stdout.strip()
            if version:
                return f"{version}"
            else:
                return f"0.0.0"
        else:
            return f"{tool}: Error executing command"
    except Exception as e:
        return f"{tool}: {str(e)}"

# Function to load the tool version config and fetch versions for each tool
def get_tool_versions():
    tool_versions = {}
    
    try:
        with open(TOOL_VERSION_CONFIG, 'r') as f:
            tools_config = json.load(f)

        # Loop through each tool in the config and fetch its version
        for tool, details in tools_config.items():
            command = details.get('command', '')
            if command:
                tool_versions[tool] = get_version(tool, command)
            else:
                tool_versions[tool] = f"{tool}: No command found in config"
    
    except FileNotFoundError:
        print(f"Error: {TOOL_VERSION_CONFIG} file not found")
    except json.JSONDecodeError:
        print(f"Error: Failed to parse {TOOL_VERSION_CONFIG}, invalid JSON")
    
    # Write the results to a file
    with open(OUTPUT_FILE, 'w') as outfile:
        json.dump(tool_versions, outfile, indent=4)
    
    print(f"Tool versions saved to {OUTPUT_FILE}")
    
def run_docker_tests(image_name):
    container_name = f"test-container-{int(time.time())}"
    container_tmp_dir = "/tmp/test_tools"  # Working directory inside the container
    host_config_file = os.path.abspath("./tool_version_config.json")  # Path to the tool version config file on the host
    host_tool_version_output = os.path.abspath("./tool_versions.json")  # Path to store the tool version output file

    # Log to store any errors
    error_log = []

    def safe_subprocess_call(command, description):
        try:
            print(f"Running: {description}...")
            subprocess.check_call(command)
        except subprocess.CalledProcessError as e:
            error_log.append(f"Error during {description}: {e}")
            print(f"Error during {description}: {e}")
            
    check_cmd = ["docker", "images", "-q", image_name]
    result = subprocess.run(check_cmd, capture_output=True, text=True)
    
    if result.stdout.strip():
        print(f"Image '{image_name}' already exists locally.")
    else:
        print(f"Image '{image_name} not found locally, Pulling from remote...")
        safe_subprocess_call(["docker", "pull", image_name], "pull Docker image")

    # Start the container in detached mode
    safe_subprocess_call(["docker", "run", "-d", "--user", "runner", "--name", container_name, image_name, "tail", "-f", "/dev/null"], "start Docker container")

    # Prepare /tmp/test_tools directory inside the container
    safe_subprocess_call(["docker", "exec", container_name, "mkdir", "-p", container_tmp_dir], "prepare /tmp/test_tools directory")
    safe_subprocess_call(["docker", "exec", container_name, "chmod", "777", container_tmp_dir], "set permissions for /tmp/test_tools directory")

    # Copy test scripts and tool_version_config.json to /tmp folder inside the container
    safe_subprocess_call(["docker", "cp", host_config_file, f"{container_name}:{container_tmp_dir}/tool_version_config.json"], "copy tool_version_config.json")

    # Verify the files inside the container by listing the contents of /tmp/test_tools
    safe_subprocess_call(["docker", "exec", container_name, "ls", "-la", container_tmp_dir], "list contents of /tmp/test_tools")

    # Run get_tool_version.py to fetch the tool versions
    get_tool_versions()

    # Copy the tool versions output file back to the host
    safe_subprocess_call(["docker", "cp", f"{container_name}:{container_tmp_dir}/tool_versions.json", host_tool_version_output], "copy tool versions output")

    print(f"Tool versions saved at {host_tool_version_output}")

    # Log errors if any
    if error_log:
        print("Errors occurred during the execution:")
        for log in error_log:
            print(log)

    # Stop and remove the container
    safe_subprocess_call(["docker", "stop", container_name], "stop container")
    safe_subprocess_call(["docker", "rm", container_name], "remove container")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python test_manager.py <docker_image_name>")
        sys.exit(1)

    docker_image_name = sys.argv[1]
    run_docker_tests(docker_image_name)
