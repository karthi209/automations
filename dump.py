import subprocess
import os
import re

def test_maven():
    tool_command = "mvn"
    version_regex = r"(?<=Maven )\d+\.\d+\.\d+"

    try:
        version_output = subprocess.check_output([tool_command, "--version"], stderr=subprocess.STDOUT).decode()
        match = re.search(version_regex, version_output)
        if match:
            version = match.group(0)
        else:
            version = "Version not found using regex"
        
        install_path = subprocess.check_output(["which", tool_command], stderr=subprocess.STDOUT).decode().strip()
        symlink = "No symlink"  # Add symlink logic if necessary
        
        return {
            "tool": "maven",
            "version": version,
            "install_path": install_path,
            "symlink": symlink
        }
    except subprocess.CalledProcessError:
        return {"tool": "maven", "version": "not installed", "install_path": "not found", "symlink": "not found"}




import subprocess
import os

def test_curl():
    tool_command = "curl"
    try:
        version_output = subprocess.check_output([tool_command, "--version"], stderr=subprocess.STDOUT).decode()
        version = version_output.strip()
        install_path = subprocess.check_output(["which", tool_command], stderr=subprocess.STDOUT).decode().strip()
        symlink = "No symlink"  # Add symlink logic if necessary
        
        return {
            "tool": "curl",
            "version": version,
            "install_path": install_path,
            "symlink": symlink
        }
    except subprocess.CalledProcessError:
        return {"tool": "curl", "version": "not installed", "install_path": "not found", "symlink": "not found"}





import json
import os
from test_python3 import test_python3
from test_maven import test_maven
from test_curl import test_curl

def main():
    tools_info = []
    
    # Run each tool test
    tools_info.append(test_python3())
    tools_info.append(test_maven())
    tools_info.append(test_curl())

    # Write the results to a JSON file
    with open('/tool_test_results.json', 'w') as f:
        json.dump(tools_info, f, indent=4)

    # Print the results
    for tool_info in tools_info:
        print(f"Results for {tool_info['tool']}:")
        print(f"  Version: {tool_info['version']}")
        print(f"  Installation Path: {tool_info['install_path']}")
        print(f"  Symlink: {tool_info['symlink']}")

if __name__ == "__main__":
    main()





import subprocess
import sys
import os
import time

def run_docker_container(image_name, test_files):
    # Generate a random container name to avoid conflicts
    container_name = f"test-container-{int(time.time())}"
    
    try:
        # Pull the Docker image (if not already pulled)
        print(f"Pulling Docker image {image_name}...")
        subprocess.check_call(["docker", "pull", image_name])

        # Run the container
        print(f"Starting container {container_name}...")
        subprocess.check_call([
            "docker", "run", "-d", "--name", container_name, image_name, "tail", "-f", "/dev/null"
        ])
        
        # Copy test files to the container
        print("Copying test files to the container...")
        for src, dest in test_files.items():
            subprocess.check_call(["docker", "cp", src, f"{container_name}:{dest}"])

        # Run the test scripts in the container
        print("Running tests inside the container...")
        subprocess.check_call([
            "docker", "exec", container_name, "python3", "/test_tools/test_tools.py"
        ])

        # Capture the results
        print("Test completed.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    finally:
        # Stop and remove the container
        print(f"Stopping and removing container {container_name}...")
        subprocess.check_call(["docker", "stop", container_name])
        subprocess.check_call(["docker", "rm", container_name])


if __name__ == "__main__":
    image_name = sys.argv[1]  # Docker image name
    test_files = {
        "test_tools/test_python3.py": "/test_tools/test_python3.py",
        "test_tools/test_maven.py": "/test_tools/test_maven.py",
        "test_tools/test_curl.py": "/test_tools/test_curl.py",
        "test_tools/test_tools.py": "/test_tools/test_tools.py",
    }
    run_docker_container(image_name, test_files)
