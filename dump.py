import subprocess
import time
import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_docker_tests(image_name):
    container_name = f"test-container-{int(time.time())}"
    container_tmp_dir = "/tmp/test_tools"  # Working directory inside the container
    host_test_scripts_dir = os.path.abspath("./test_tools")  # Default location of test scripts on the host
    host_output_report = os.path.abspath("./test_report.json")  # Default location for the JSON report on the host

    try:
        # Pull the Docker image
        logging.info(f"Pulling Docker image {image_name}...")
        subprocess.check_call(["docker", "pull", image_name])

        # Start the container in detached mode
        logging.info(f"Starting container {container_name}...")
        subprocess.check_call(["docker", "run", "-d", "--name", container_name, image_name, "tail", "-f", "/dev/null"])

        # Prepare /tmp/test_tools directory inside the container
        logging.info("Preparing /tmp/test_tools directory inside the container...")
        subprocess.check_call(["docker", "exec", container_name, "mkdir", "-p", container_tmp_dir])
        subprocess.check_call(["docker", "exec", container_name, "chmod", "777", container_tmp_dir])

        # Copy test scripts to /tmp folder inside the container
        logging.info(f"Copying test scripts to the container at {container_tmp_dir}...")
        subprocess.check_call(["docker", "cp", host_test_scripts_dir, f"{container_name}:{container_tmp_dir}"])

        # Verify the files inside the container by listing the contents of /tmp/test_tools
        logging.info("Listing contents of /tmp/test_tools inside the container...")
        result = subprocess.check_output(["docker", "exec", container_name, "ls", "-la", container_tmp_dir])
        logging.info(f"Container contents:\n{result.decode('utf-8')}")

        # Create a virtual environment inside the container
        logging.info("Creating virtual environment in the container...")
        subprocess.check_call(["docker", "exec", container_name, "python3", "-m", "venv", f"{container_tmp_dir}/venv"])

        # Install pytest and dependencies inside the virtual environment
        logging.info("Installing pytest in the virtual environment...")
        subprocess.check_call(["docker", "exec", container_name, f"{container_tmp_dir}/venv/bin/pip", "install", "pytest", "pytest-json-report"])

        # Run pytest inside the container with JSON report generation
        logging.info("Running pytest in the container with JSON reporting...")
        subprocess.check_call(["docker", "exec", container_name, f"{container_tmp_dir}/venv/bin/pytest", container_tmp_dir,
                               "--json-report", "--json-report-file", f"{container_tmp_dir}/test_report.json"])

        # Copy the JSON report back to the host
        logging.info(f"Copying the JSON report to {host_output_report}...")
        subprocess.check_call(["docker", "cp", f"{container_name}:{container_tmp_dir}/test_report.json", host_output_report])

        logging.info(f"Test completed. Report saved at {host_output_report}")

    except subprocess.CalledProcessError as e:
        logging.error(f"Error: {e}")

    finally:
        # Stop and remove the container
        logging.info(f"Stopping and removing container {container_name}...")
        subprocess.check_call(["docker", "stop", container_name])
        subprocess.check_call(["docker", "rm", container_name])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_manager.py <docker_image_name>")
        sys.exit(1)

    docker_image_name = sys.argv[1]
    run_docker_tests(docker_image_name)





import subprocess
import pytest

# Function to fetch the tool version
def get_tool_version(tool_name):
    try:
        version = subprocess.check_output([tool_name, "--version"]).decode('utf-8').strip()
        return version
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to get {tool_name} version: {str(e)}")

# Test to verify the tool version and run your actual test logic
def test_git_version():
    git_version = get_tool_version("git")
    # Assuming you want to verify a minimum version
    assert git_version >= "2.0", f"Git version {git_version} is too old"

    # Your other tests for git functionality here
    assert subprocess.check_output(["git", "--version"])  # Simple test to verify git is functional

@pytest.mark.tool_version("git")
def test_git_tool():
    # You can call a specific test function here that checks tool functionality
    pass



[pytest]
markers =
    tool_version(name): mark the test as related to a specific tool version
