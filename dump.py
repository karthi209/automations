import subprocess
import time
import sys
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", handlers=[logging.StreamHandler()])

def run_docker_tests(image_name):
    container_name = f"test-container-{int(time.time())}"
    container_tmp_dir = "/tmp/test_tools"  # Working directory inside the container
    host_test_scripts_dir = "./test_tools"  # Default location of test scripts on the host
    host_output_report = "./test_report.json"  # Default location for the JSON report on the host
    tool_version_script = "./get_tool_version.py"  # Path to get_tool_version.py script

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

        # Copy test scripts and get_tool_version.py to /tmp folder inside the container
        logging.info(f"Copying test scripts from {host_test_scripts_dir} to the container at {container_tmp_dir}...")
        subprocess.check_call(["docker", "cp", host_test_scripts_dir, f"{container_name}:{container_tmp_dir}"])
        subprocess.check_call(["docker", "cp", tool_version_script, f"{container_name}:{container_tmp_dir}"])

        # Create a virtual environment inside the container
        logging.info("Creating virtual environment in the container...")
        subprocess.check_call(["docker", "exec", container_name, "python3", "-m", "venv", f"{container_tmp_dir}/venv"])

        # Install pytest and dependencies inside the virtual environment
        logging.info("Installing pytest in the virtual environment...")
        subprocess.check_call(["docker", "exec", container_name, f"{container_tmp_dir}/venv/bin/pip", "install", "pytest", "pytest-json-report"])

        # Run get_tool_version.py to get tool versions
        logging.info("Getting tool versions inside the container...")
        result = subprocess.check_output([
            "docker", "exec", container_name, f"{container_tmp_dir}/venv/bin/python", f"{container_tmp_dir}/get_tool_version.py"
        ])
        tool_versions = result.decode("utf-8").strip()

        # Run pytest inside the container with JSON report generation
        logging.info("Running pytest in the container with JSON reporting...")
        subprocess.check_call([
            "docker", "exec", container_name, f"{container_tmp_dir}/venv/bin/pytest", container_tmp_dir,
            "--json-report", "--json-report-file", f"{container_tmp_dir}/test_report.json"
        ])

        # Copy the JSON report back to the host
        logging.info(f"Copying the JSON report to {host_output_report}...")
        subprocess.check_call(["docker", "cp", f"{container_name}:{container_tmp_dir}/test_report.json", host_output_report])

        # Add tool version metadata to the JSON report
        with open(host_output_report, "r") as report_file:
            report_data = json.load(report_file)

        # Add tool version metadata
        report_data["metadata"] = {
            "tool_versions": tool_versions
        }

        # Save updated JSON report
        with open(host_output_report, "w") as report_file:
            json.dump(report_data, report_file, indent=4)

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
        logging.error("Usage: python test_manager.py <docker_image_name>")
        sys.exit(1)

    docker_image_name = sys.argv[1]
    run_docker_tests(docker_image_name)
