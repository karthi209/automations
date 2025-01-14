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

    # Log to store any errors
    error_log = []

    def safe_subprocess_call(command, description):
        try:
            print(f"Running: {description}...")
            subprocess.check_call(command)
        except subprocess.CalledProcessError as e:
            error_log.append(f"Error during {description}: {e}")
            print(f"Error during {description}: {e}")

    # Pull the Docker image
    safe_subprocess_call(["docker", "pull", image_name], "pull Docker image")

    # Start the container in detached mode
    safe_subprocess_call(["docker", "run", "-d", "--name", container_name, image_name, "tail", "-f", "/dev/null"], "start Docker container")

    # Prepare /tmp/test_tools directory inside the container
    safe_subprocess_call(["docker", "exec", container_name, "mkdir", "-p", container_tmp_dir], "prepare /tmp/test_tools directory")
    safe_subprocess_call(["docker", "exec", container_name, "chmod", "777", container_tmp_dir], "set permissions for /tmp/test_tools directory")

    # Copy test scripts and tool_version_config.json to /tmp folder inside the container
    safe_subprocess_call(["docker", "cp", host_test_scripts_dir, f"{container_name}:{container_tmp_dir}"], "copy test scripts")
    safe_subprocess_call(["docker", "cp", host_config_file, f"{container_name}:{container_tmp_dir}/tool_version_config.json"], "copy tool_version_config.json")
    safe_subprocess_call(["docker", "cp", host_get_tool_version_script, f"{container_name}:{container_tmp_dir}/get_tool_version.py"], "copy get_tool_version.py script")

    # Verify the files inside the container by listing the contents of /tmp/test_tools
    safe_subprocess_call(["docker", "exec", container_name, "ls", "-la", container_tmp_dir], "list contents of /tmp/test_tools")

    # Run get_tool_version.py to fetch the tool versions
    safe_subprocess_call(["docker", "exec", container_name, "python3", f"{container_tmp_dir}/get_tool_version.py"], "run get_tool_version.py")

    # Copy the tool versions output file back to the host
    safe_subprocess_call(["docker", "cp", f"{container_name}:{container_tmp_dir}/tool_versions.json", host_tool_version_output], "copy tool versions output")

    # Create a virtual environment inside the container
    safe_subprocess_call(["docker", "exec", container_name, "python3", "-m", "venv", f"{container_tmp_dir}/venv"], "create virtual environment")

    # Install pytest and dependencies inside the virtual environment
    safe_subprocess_call(["docker", "exec", container_name, f"{container_tmp_dir}/venv/bin/pip", "install", "pytest", "pytest-json-report"], "install pytest")

    # Run pytest inside the container with JSON report generation
    safe_subprocess_call(["docker", "exec", container_name, f"{container_tmp_dir}/venv/bin/pytest", container_tmp_dir,
                          "--json-report", "--json-report-file", f"{container_tmp_dir}/test_report.json"], "run pytest with JSON reporting")

    # Copy the JSON report back to the host
    safe_subprocess_call(["docker", "cp", f"{container_name}:{container_tmp_dir}/test_report.json", host_output_report], "copy JSON report to host")

    print(f"Test completed. Report saved at {host_output_report}")
    print(f"Tool versions saved at {host_tool_version_output}")

    # Log errors if any
    if error_log:
        print("Errors occurred during the execution:")
        for log in error_log:
            print(log)

    # Stop and remove the container
    safe_subprocess_call(["docker", "stop", container_name], "stop container")
    safe_subprocess_call(["docker", "rm", container_name], "remove container")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_manager.py <docker_image_name>")
        sys.exit(1)

    docker_image_name = sys.argv[1]
    run_docker_tests(docker_image_name)
