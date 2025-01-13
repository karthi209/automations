import subprocess
import sys
import os
import time

def run_docker_container(image_name, test_dir):
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
        
        # Copy the test directory to the container
        print(f"Copying {test_dir} to the container...")
        subprocess.check_call(["docker", "cp", test_dir, f"{container_name}:/test_tools"])

        # Run each test script inside the container
        test_files = os.listdir(test_dir)
        for test_script in test_files:
            test_script_path = f"/test_tools/{test_script}"
            print(f"Running test: {test_script_path}...")
            subprocess.check_call([
                "docker", "exec", container_name, "python3", test_script_path
            ])

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
    test_dir = "test_tools"   # Path to the test folder containing unit tests
    run_docker_container(image_name, test_dir)
