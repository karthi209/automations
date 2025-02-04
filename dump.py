import subprocess
import json
import time
import sys
import os

TOOL_VERSION_CONFIG = 'tool_version_config.json'
OUTPUT_FILE = 'output.json'  # Output file location inside the container

def run_docker_tests(image_name):
    container_name = f"test-container-{int(time.time())}"
    container_tmp_dir = "/tmp/test_tools"  # Working directory inside the container
    host_test_scripts_dir = os.path.abspath("./test_tools")  
    host_output_report = os.path.abspath("./test_report.json")  
    host_config_file = os.path.abspath("./tool_version_config.json")  
    host_get_tool_version_script = os.path.abspath("./get_tool_version.py")  
    host_tool_version_output = os.path.abspath("./tool_versions.json")  

    error_log = []

    def safe_subprocess_call(command, description):
        try:
            print(f"Running: {description}...")
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            error_log.append(f"Error during {description}: {e}")
            print(f"Error during {description}: {e}")

    # Check if the Docker image exists
    check_cmd = ["docker", "images", "-q", image_name]
    result = subprocess.run(check_cmd, capture_output=True, text=True)

    if not result.stdout.strip():
        print(f"Image '{image_name}' not found locally. Pulling from remote...")
        safe_subprocess_call(["docker", "pull", image_name], "pull Docker image")

    # Run the container in detached mode
    safe_subprocess_call(
        ["docker", "run", "-d", "--user", "runner", "--name", container_name, image_name, "tail", "-f", "/dev/null"],
        "start Docker container"
    )

    # Setup /tmp/test_tools in the container
    safe_subprocess_call(["docker", "exec", container_name, "mkdir", "-p", container_tmp_dir], "create /tmp/test_tools directory")
    safe_subprocess_call(["docker", "exec", container_name, "chmod", "777", container_tmp_dir], "set permissions for /tmp/test_tools")

    # Copy test scripts and config files into the container
    safe_subprocess_call(["docker", "cp", host_test_scripts_dir, f"{container_name}:{container_tmp_dir}"], "copy test scripts")
    safe_subprocess_call(["docker", "cp", host_config_file, f"{container_name}:{container_tmp_dir}/tool_version_config.json"], "copy tool_version_config.json")
    safe_subprocess_call(["docker", "cp", host_get_tool_version_script, f"{container_name}:{container_tmp_dir}/get_tool_version.py"], "copy get_tool_version.py")

    # Verify copied files
    safe_subprocess_call(["docker", "exec", container_name, "ls", "-la", container_tmp_dir], "list contents of /tmp/test_tools")

    # Run the tool version collection script inside the container
    safe_subprocess_call(["docker", "exec", container_name, "python3", f"{container_tmp_dir}/get_tool_version.py"], "run get_tool_version.py")

    # Copy the tool versions output file back to the host
    safe_subprocess_call(["docker", "cp", f"{container_name}:{container_tmp_dir}/tool_versions.json", host_tool_version_output], "copy tool versions output")

    # Setup Python virtual environment inside the container
    safe_subprocess_call(["docker", "exec", container_name, "python3", "-m", "venv", f"{container_tmp_dir}/venv"], "create virtual environment")

    # Install pytest inside the virtual environment
    safe_subprocess_call(["docker", "exec", container_name, f"{container_tmp_dir}/venv/bin/pip", "install", "pytest", "pytest-json-report"], "install pytest")

    # Run pytest inside the container and generate a JSON report
    safe_subprocess_call([
        "docker", "exec", container_name, f"{container_tmp_dir}/venv/bin/pytest", container_tmp_dir,
        "--json-report", "--json-report-file", f"{container_tmp_dir}/test_report.json"
    ], "run pytest with JSON reporting")

    # Copy the JSON report back to the host
    safe_subprocess_call(["docker", "cp", f"{container_name}:{container_tmp_dir}/test_report.json", host_output_report], "copy JSON report to host")

    print(f"Test completed. Report saved at {host_output_report}")
    print(f"Tool versions saved at {host_tool_version_output}")

    # Stop and remove the container
    safe_subprocess_call(["docker", "stop", container_name], "stop container")
    safe_subprocess_call(["docker", "rm", container_name], "remove container")

    if error_log:
        print("\nErrors occurred during execution:")
        for log in error_log:
            print(log)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python run_docker_tests.py <docker-image>")
        sys.exit(1)

    docker_image = sys.argv[1]
    run_docker_tests(docker_image)
