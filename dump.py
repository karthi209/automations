import subprocess
import time
import sys
import os

def run_docker_tests(image_name):
    container_name = f"test-container-{int(time.time())}"
    container_tmp_dir = "/tmp/test_tools"  # Working directory inside the container
    host_test_scripts_dir = os.path.abspath("./test_tools")  # Default location of test scripts on the host
    host_output_report = os.path.abspath("./test_report.json")  # Default location for the JSON report on the host
    host_config_file = os.path.abspath("./tool_version_config.json")  # Path to the tool version config file on the host
    host_get_tool_version_script = os.path.abspath("./get_tool_version.py")  # Path to the get_tool_version.py script
    host_tool_version_output = os.path.abspath("./tool_versions.json")  # Path to store the tool version output file
    host_pytest_ini = os.path.abspath("./pytest.ini")  # Path to the pytest.ini configuration file

    try:
        # Pull the Docker image
        print(f"Pulling Docker image {image_name}...")
        subprocess.check_call(["docker", "pull", image_name])

        # Start the container in detached mode
        print(f"Starting container {container_name}...")
        subprocess.check_call(["docker", "run", "-d", "--name", container_name, image_name, "tail", "-f", "/dev/null"])

        # Prepare /tmp/test_tools directory inside the container
        print("Preparing /tmp/test_tools directory inside the container...")
        subprocess.check_call(["docker", "exec", container_name, "mkdir", "-p", container_tmp_dir])
        subprocess.check_call(["docker", "exec", container_name, "chmod", "777", container_tmp_dir])

        # Copy test scripts, tool_version_config.json, get_tool_version.py, and pytest.ini to the container
        print(f"Copying test scripts, tool_version_config.json, get_tool_version.py, and pytest.ini to the container at {container_tmp_dir}...")
        subprocess.check_call(["docker", "cp", host_test_scripts_dir, f"{container_name}:{container_tmp_dir}"])
        subprocess.check_call(["docker", "cp", host_config_file, f"{container_name}:{container_tmp_dir}/tool_version_config.json"])
        subprocess.check_call(["docker", "cp", host_get_tool_version_script, f"{container_name}:{container_tmp_dir}/get_tool_version.py"])
        subprocess.check_call(["docker", "cp", host_pytest_ini, f"{container_name}:{container_tmp_dir}/pytest.ini"])

        # Verify the files inside the container by listing the contents of /tmp/test_tools
        print("Listing contents of /tmp/test_tools inside the container...")
        result = subprocess.check_output(["docker", "exec", container_name, "ls", "-la", container_tmp_dir])
        print(f"Container contents:\n{result.decode('utf-8')}")

        # Run pytest inside the container with JSON report generation
        print("Running pytest in the container with JSON reporting...")
        subprocess.check_call(["docker", "exec", container_name, "pytest", container_tmp_dir,
                               "--json-report", "--json-report-file", f"{container_tmp_dir}/test_report.json"])

        # Copy the JSON report back to the host
        print(f"Copying the JSON report to {host_output_report}...")
        subprocess.check_call(["docker", "cp", f"{container_name}:{container_tmp_dir}/test_report.json", host_output_report])

        print(f"Test completed. Report saved at {host_output_report}")
        print(f"Tool versions saved at {host_tool_version_output}")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    finally:
        # Stop and remove the container
        print(f"Stopping and removing container {container_name}...")
        subprocess.check_call(["docker", "stop", container_name])
        subprocess.check_call(["docker", "rm", container_name])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_manager.py <docker_image_name>")
        sys.exit(1)

    docker_image_name = sys.argv[1]
    run_docker_tests(docker_image_name)
