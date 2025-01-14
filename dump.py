import subprocess
import time
import os

def run_docker_tests(image_name, test_scripts_dir, output_report):
    container_name = f"test-container-{int(time.time())}"

    try:
        # Pull the Docker image
        print(f"Pulling Docker image {image_name}...")
        subprocess.check_call(["docker", "pull", image_name])

        # Start the container
        print(f"Starting container {container_name}...")
        subprocess.check_call([
            "docker", "run", "-d", "--name", container_name, image_name, "tail", "-f", "/dev/null"
        ])

        # Copy test scripts into the container
        print(f"Copying test scripts from {test_scripts_dir} to the container...")
        subprocess.check_call(["docker", "cp", test_scripts_dir, f"{container_name}:/test_tools"])

        # Install pytest and dependencies inside the container
        print("Installing pytest inside the container...")
        subprocess.check_call([
            "docker", "exec", container_name, "pip3", "install", "pytest", "pytest-json-report"
        ])

        # Run pytest with JSON reporting in the container
        print("Running pytest in the container with JSON reporting...")
        subprocess.check_call([
            "docker", "exec", container_name, "pytest", "/test_tools",
            "--json-report", "--json-report-file", "/test_tools/test_report.json"
        ])

        # Copy the JSON report back to the host
        print(f"Copying the JSON report to {output_report}...")
        subprocess.check_call(["docker", "cp", f"{container_name}:/test_tools/test_report.json", output_report])

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    finally:
        # Stop and remove the container
        print(f"Stopping and removing container {container_name}...")
        subprocess.check_call(["docker", "stop", container_name])
        subprocess.check_call(["docker", "rm", container_name])


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python test_manager.py <docker_image_name> <test_scripts_dir> <output_report>")
        sys.exit(1)

    docker_image_name = sys.argv[1]
    test_scripts_directory = sys.argv[2]
    output_report_file = sys.argv[3]

    run_docker_tests(docker_image_name, test_scripts_directory, output_report_file)
