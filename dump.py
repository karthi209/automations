import subprocess
import sys
import time
import os

def run_docker_container(image_name, test_folder):
    container_name = f"test-container-{int(time.time())}"
    
    try:
        # Pull the Docker image (if not already pulled)
        print(f"Pulling Docker image {image_name}...")
        subprocess.check_call(["docker", "pull", image_name])

        # Run the container in detached mode (keeping it alive)
        print(f"Starting container {container_name}...")
        subprocess.check_call([
            "docker", "run", "-d", "--name", container_name, image_name, "tail", "-f", "/dev/null"
        ])
        
        # Create pyenv and install dependencies
        print("Setting up Python virtual environment and installing pytest...")
        subprocess.check_call([
            "docker", "exec", container_name, "bash", "-c", 
            "python3 -m venv /tmp/pyenv && "
            "source /tmp/pyenv/bin/activate && "
            "pip install --upgrade pip && "
            "pip install pytest"
        ])
        
        # Copy the entire test_tools folder to /tmp in the container
        print(f"Copying the test tools folder to {container_name}:/tmp/test_tools")
        subprocess.check_call(["docker", "cp", test_folder, f"{container_name}:/tmp/test_tools"])

        # Verify the files are correctly copied into the container
        print("Verifying copied files in the container...")
        subprocess.check_call(["docker", "exec", container_name, "ls", "/tmp/test_tools"])

        # Run the test scripts inside the container (from the /tmp/test_tools folder)
        print("Running tests inside the container...")
        subprocess.check_call([
            "docker", "exec", container_name, "bash", "-c", 
            "source /tmp/pyenv/bin/activate && "
            "pytest --json-report --json-report-file=/tmp/test_tools/result.json /tmp/test_tools"
        ])
        
        print("Test completed.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    finally:
        # Stop and remove the container after testing
        print(f"Stopping and removing container {container_name}...")
        subprocess.check_call(["docker", "stop", container_name])
        subprocess.check_call(["docker", "rm", container_name])


if __name__ == "__main__":
    image_name = sys.argv[1]  # Docker image name
    test_folder = "test_tools"  # Folder with the test files
    run_docker_container(image_name, test_folder)
