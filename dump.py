import subprocess
import sys
import time
import os

def get_test_files(test_folder):
    # Discover all Python test files in the test folder
    test_files = {}
    for file_name in os.listdir(test_folder):
        if file_name.endswith(".py"):
            test_files[file_name] = f"/test_tools/{file_name}"
    return test_files

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
        
        # Get the test files dynamically from the folder
        test_files = get_test_files(test_folder)
        
        # Copy the test files to the container
        print("Copying test files to the container...")
        for src, dest in test_files.items():
            src_path = os.path.join(test_folder, src)
            print(f"Copying {src_path} to {container_name}:{dest}")
            subprocess.check_call(["docker", "cp", src_path, f"{container_name}:{dest}"])

        # Run the test scripts inside the container
        print("Running tests inside the container...")
        subprocess.check_call([
            "docker", "exec", container_name, "pytest", "--json-report", "--json-report-file=result.json", "/test_tools"
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
