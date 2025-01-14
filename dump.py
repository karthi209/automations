import subprocess
import time
import sys

def run_docker_tests(image_name):
    container_name = f"test-container-{int(time.time())}"
    container_tmp_dir = "/tmp/test_tools"  # Working directory inside the container
    host_test_scripts_dir = "./test_tools"  # Default location of test scripts on the host
    host_output_report = "./test_report.json"  # Default location for the JSON report on the host

    try:
        # Pull the Docker image
        print(f"Pulling Docker image {image_name}...")
        subprocess.check_call(["docker", "pull", image_name])

        # Start the container in detached mode
        print(f"Starting container {container_name}...")
        subprocess.check_call([
            "docker", "run", "-d", "--name", container_name, image_name, "tail", "-f", "/dev/null"
        ])

        # Prepare /tmp/test_tools directory inside the container
        print("Preparing /tmp/test_tools directory inside the container...")
        subprocess.check_call([
            "docker", "exec", container_name, "mkdir", "-p", container_tmp_dir
        ])
        subprocess.check_call([
            "docker", "exec", container_name, "chmod", "777", container_tmp_dir
        ])

        # Copy test scripts to /tmp folder inside the container
        print(f"Copying test scripts from {host_test_scripts_dir} to the container at {container_tmp_dir}...")
        subprocess.check_call(["docker", "cp", host_test_scripts_dir, f"{container_name}:{container_tmp_dir}"])

        # Create a virtual environment inside the container
        print("Creating virtual environment in the container...")
        subprocess.check_call([
            "docker", "exec", container_name, "python3", "-m", "venv", f"{container_tmp_dir}/venv"
        ])

        # Install pytest and dependencies inside the virtual environment
        print("Installing pytest in the virtual environment...")
        subprocess.check_call([
            "docker", "exec", container_name, f"{container_tmp_dir}/venv/bin/pip", "install", "pytest", "pytest-json-report"
        ])

        # Run pytest inside the container with JSON report generation
        print("Running pytest in the container with JSON reporting...")
        subprocess.check_call([
            "docker", "exec", container_name, f"{container_tmp_dir}/venv/bin/pytest", container_tmp_dir,
            "--json-report", "--json-report-file", f"{container_tmp_dir}/test_report.json"
        ])

        # Copy the JSON report back to the host
        print(f"Copying the JSON report to {host_output_report}...")
        subprocess.check_call(["docker", "cp", f"{container_name}:{container_tmp_dir}/test_report.json", host_output_report])

        print(f"Test completed. Report saved at {host_output_report}")
    
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
