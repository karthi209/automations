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




import os
import subprocess

def test_git_version():
    result = subprocess.run(["git", "--version"], capture_output=True, text=True)
    assert result.returncode == 0, "Git is not installed or not functioning correctly."
    assert "git version" in result.stdout, "Git version not found in output."

def test_git_install_path():
    result = subprocess.run(["which", "git"], capture_output=True, text=True)
    assert result.returncode == 0, "Git is not installed in PATH."
    install_path = result.stdout.strip()
    assert os.path.exists(install_path), f"Git installation path {install_path} does not exist."

def test_git_symlink():
    result = subprocess.run(["which", "git"], capture_output=True, text=True)
    assert result.returncode == 0, "Git is not installed in PATH."
    install_path = result.stdout.strip()
    if os.path.islink(install_path):
        symlink_target = os.readlink(install_path)
        assert os.path.exists(symlink_target), f"Symlink target {symlink_target} does not exist."



import os
import subprocess

def test_maven_version():
    result = subprocess.run(["mvn", "--version"], capture_output=True, text=True)
    assert result.returncode == 0, "Maven is not installed or not functioning correctly."
    assert "Apache Maven" in result.stdout, "Maven version not found in output."

def test_maven_install_path():
    result = subprocess.run(["which", "mvn"], capture_output=True, text=True)
    assert result.returncode == 0, "Maven is not installed in PATH."
    install_path = result.stdout.strip()
    assert os.path.exists(install_path), f"Maven installation path {install_path} does not exist."
