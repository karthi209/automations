import subprocess
import time
import sys
import os
import glob
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def find_test_scripts(base_path):
    """
    Locate all test scripts within the collections directory.
    """
    test_files = glob.glob(os.path.join(base_path, "collections/devsecops/*/test/test_default.py"))
    if not test_files:
        logging.warning(f"No test scripts found in {base_path}/collections/devsecops/")
    return test_files

def run_docker_tests(image_name):
    container_name = f"test-container-{int(time.time())}"
    container_tmp_dir = "/tmp/test_tools"  # Working directory inside the container
    host_base_dir = os.path.abspath(".")  # Base directory of the script
    host_output_report = os.path.abspath("./test_report.json")  # Default location for the JSON report on the host
    host_config_file = os.path.abspath("./tool_version_config.json")  # Path to the tool version config file on the host
    host_get_tool_version_script = os.path.abspath("./get_tool_version.py")  # Path to the get_tool_version.py script
    host_tool_version_output = os.path.abspath("./tool_versions.json")  # Path to store the tool version output file

    error_log = []

    def safe_subprocess_call(command, description):
        try:
            logging.info(f"Running: {description}...")
            subprocess.check_call(command)
        except subprocess.CalledProcessError as e:
            error_log.append(f"Error during {description}: {e}")
            logging.error(f"Error during {description}: {e}")

    try:
        # Locate test scripts dynamically
        test_files = find_test_scripts(host_base_dir)
        if not test_files:
            logging.error("No test scripts found. Exiting.")
            return

        # Pull the Docker image
        safe_subprocess_call(["docker", "pull", image_name], "pull Docker image")

        # Start the container in detached mode
        safe_subprocess_call(
            ["docker", "run", "-d", "--user", "runner", "--name", container_name, image_name, "tail", "-f", "/dev/null"],
            "start Docker container"
        )

        # Prepare /tmp/test_tools directory inside the container
        safe_subprocess_call(["docker", "exec", container_name, "mkdir", "-p", container_tmp_dir], "prepare test_tools directory")
        safe_subprocess_call(["docker", "exec", container_name, "chmod", "777", container_tmp_dir], "set permissions for test_tools directory")

        # Copy test scripts to the container
        for test_file in test_files:
            safe_subprocess_call(["docker", "cp", test_file, f"{container_name}:{container_tmp_dir}/"], f"copy {test_file}")

        # Copy additional files (config and script) to the container
        safe_subprocess_call(["docker", "cp", host_config_file, f"{container_name}:{container_tmp_dir}/tool_version_config.json"], "copy tool_version_config.json")
        safe_subprocess_call(["docker", "cp", host_get_tool_version_script, f"{container_name}:{container_tmp_dir}/get_tool_version.py"], "copy get_tool_version.py script")

        # Verify contents
        safe_subprocess_call(["docker", "exec", container_name, "ls", "-la", container_tmp_dir], "list contents of test_tools")

        # Run get_tool_version.py
        safe_subprocess_call(["docker", "exec", container_name, "python3", f"{container_tmp_dir}/get_tool_version.py"], "run get_tool_version.py")

        # Copy tool versions output
        safe_subprocess_call(["docker", "cp", f"{container_name}:{container_tmp_dir}/tool_versions.json", host_tool_version_output], "copy tool versions output")

        # Create virtual environment and install pytest
        safe_subprocess_call(["docker", "exec", container_name, "python3", "-m", "venv", f"{container_tmp_dir}/venv"], "create virtual environment")
        safe_subprocess_call(["docker", "exec", container_name, f"{container_tmp_dir}/venv/bin/pip", "install", "pytest", "pytest-json-report"], "install pytest")

        # Run pytest with JSON reporting
        safe_subprocess_call([
            "docker", "exec", container_name, f"{container_tmp_dir}/venv/bin/pytest", container_tmp_dir,
            "--json-report", "--json-report-file", f"{container_tmp_dir}/test_report.json"
        ], "run pytest with JSON reporting")

        # Copy JSON report back to the host
        safe_subprocess_call(["docker", "cp", f"{container_name}:{container_tmp_dir}/test_report.json", host_output_report], "copy JSON report to host")

        logging.info(f"Test completed. Report saved at {host_output_report}")
        logging.info(f"Tool versions saved at {host_tool_version_output}")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        # Ensure container is stopped and removed
        safe_subprocess_call(["docker", "stop", container_name], "stop container")
        safe_subprocess_call(["docker", "rm", container_name], "remove container")

        if error_log:
            logging.error("Errors occurred during the execution:")
            for log in error_log:
                logging.error(log)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Usage: python test_manager.py <docker_image_name>")
        sys.exit(1)

    docker_image_name = sys.argv[1]
    run_docker_tests(docker_image_name)