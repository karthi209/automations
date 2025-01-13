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





import subprocess

def test_python3():
    # Check the version of Python
    version = subprocess.check_output(["python3", "--version"]).decode("utf-8").strip()
    print(f"Python version: {version}")

    # Check installation path
    install_path = subprocess.check_output(["which", "python3"]).decode("utf-8").strip()
    print(f"Python installation path: {install_path}")

    # Check if it's a symlink
    symlink = subprocess.check_output(["ls", "-l", "/usr/bin/python3"]).decode("utf-8").strip()
    print(f"Python symlink info: {symlink}")

if __name__ == "__main__":
    test_python3()





import subprocess

def test_maven():
    # Check Maven version
    version = subprocess.check_output(["mvn", "--version"]).decode("utf-8").strip()
    print(f"Maven version: {version}")

    # Check installation path
    install_path = subprocess.check_output(["which", "mvn"]).decode("utf-8").strip()
    print(f"Maven installation path: {install_path}")

    # Check if it's a symlink (if applicable)
    symlink = subprocess.check_output(["ls", "-l", "/usr/bin/mvn"]).decode("utf-8").strip()
    print(f"Maven symlink info: {symlink}")

if __name__ == "__main__":
    test_maven()





import subprocess

def test_curl():
    # Check cURL version
    version = subprocess.check_output(["curl", "--version"]).decode("utf-8").strip()
    print(f"cURL version: {version}")

    # Check installation path
    install_path = subprocess.check_output(["which", "curl"]).decode("utf-8").strip()
    print(f"cURL installation path: {install_path}")

    # Check if it's a symlink (if applicable)
    symlink = subprocess.check_output(["ls", "-l", "/usr/bin/curl"]).decode("utf-8").strip()
    print(f"cURL symlink info: {symlink}")

if __name__ == "__main__":
    test_curl()
