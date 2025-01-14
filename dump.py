import json
import subprocess
import os
import docker
import random
import string
import argparse
from pathlib import Path

# Paths
TEST_REPORT_PATH = '/tmp/test_tools/.report.json'
TOOL_VERSION_PATH = '/tmp/test_tools/tool_version.json'
OUTPUT_REPORT_PATH = '/tmp/test_tools/final_report.md'
TEST_FILES_DIR = '/path/to/test_files'  # Modify this with the correct path
TEST_CONTAINER_DIR = '/tmp/test_tools'

SUCCESS_ICON = "✅"
FAILURE_ICON = "❌"

def random_container_name():
    """Generate a random Docker container name."""
    return "test_container_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def spin_up_container(image_name, container_name):
    """Spin up a Docker container in detached mode and keep it alive."""
    client = docker.from_env()
    try:
        container = client.containers.run(
            image=image_name,
            name=container_name,
            command="tail -f /dev/null",  # Keeps the container running
            detach=True,
            tty=True
        )
        print(f"Container {container_name} started.")
        return container
    except Exception as e:
        print(f"Error spinning up container: {e}")
        return None

def setup_virtualenv(container):
    """Set up a virtual environment and install required Python packages inside the container."""
    try:
        # Command to create and activate a virtual environment inside the container
        commands = [
            "python3 -m venv /tmp/test_tools/venv",
            "source /tmp/test_tools/venv/bin/activate",
            "pip install -r /tmp/test_tools/requirements.txt"
        ]
        setup_command = " && ".join(commands)
        result = container.exec_run(f"bash -c '{setup_command}'")
        print(result.output.decode())
    except Exception as e:
        print(f"Error setting up virtual environment: {e}")

def copy_test_files(container):
    """Copy test files into the container."""
    try:
        for root, dirs, files in os.walk(TEST_FILES_DIR):
            for file in files:
                local_path = os.path.join(root, file)
                container_path = os.path.join(TEST_CONTAINER_DIR, file)
                with open(local_path, "rb") as f:
                    container.put_archive(TEST_CONTAINER_DIR, f.read())
        print("Test files copied successfully.")
    except Exception as e:
        print(f"Error copying test files: {e}")

def run_tests(container):
    """Run pytest inside the container and generate a JSON report."""
    try:
        # Running the pytest command in the virtual environment inside the container
        command = f"source /tmp/test_tools/venv/bin/activate && pytest {TEST_CONTAINER_DIR} --json-report --json-report-file={TEST_REPORT_PATH}"
        result = container.exec_run(command)
        print(result.output.decode())
        return TEST_REPORT_PATH
    except Exception as e:
        print(f"Error running tests: {e}")
        return None

def get_tool_versions(container):
    """Get tool versions inside the container."""
    tools = ["git", "python", "node", "docker"]
    versions = {}
    for tool in tools:
        try:
            result = container.exec_run(f"{tool} --version")
            output = result.output.decode().strip()
            versions[tool] = output.split()[1] if output else "Unknown version"
        except Exception as e:
            versions[tool] = "Error retrieving version"
            print(f"Error getting version for {tool}: {e}")
    with open(TOOL_VERSION_PATH, 'w') as file:
        json.dump(versions, file, indent=4)
    return versions

def extract_tool_name(nodeid):
    """Extract tool name from nodeid."""
    parts = nodeid.split('/')
    if len(parts) > 1:
        tool_part = parts[1]  # e.g., test_tools/test_git.py
        return tool_part.split('.')[0]  # e.g., git
    return "Unknown"

def generate_markdown(test_report, tool_versions):
    """Generate a Markdown report from test results and tool versions."""
    markdown = "# Test Summary Report\n\n"

    tools = {}

    for test in test_report.get('tests', []):
        nodeid = test.get('nodeid', '')
        outcome = test.get('outcome', 'unknown')
        tool_name = extract_tool_name(nodeid)
        test_name = nodeid.split('::')[-1]

        if tool_name not in tools:
            tools[tool_name] = {
                "version": tool_versions.get(tool_name, "Version not found"),
                "tests": []
            }

        icon = SUCCESS_ICON if outcome == 'passed' else FAILURE_ICON
        tools[tool_name]['tests'].append(f"{test_name} : {icon} ({outcome})")

    for tool, details in tools.items():
        markdown += f"## {tool} (Version: {details['version']})\n"
        for test_result in details['tests']:
            markdown += f"- {test_result}\n"
        markdown += "\n"

    with open(OUTPUT_REPORT_PATH, 'w') as file:
        file.write(markdown)

    print(f"Markdown report saved to {OUTPUT_REPORT_PATH}")

def main():
    parser = argparse.ArgumentParser(description="Run tests and generate a summary report.")
    parser.add_argument("--image", required=True, help="Docker image name to use for testing.")
    args = parser.parse_args()

    image_name = args.image
    container_name = random_container_name()

    # Spin up Docker container in detached mode
    container = spin_up_container(image_name, container_name)
    if not container:
        print("Failed to create container.")
        return

    try:
        # Set up virtual environment and install dependencies
        setup_virtualenv(container)

        # Copy test files
        copy_test_files(container)

        # Run tests
        test_report_path = run_tests(container)
        if not test_report_path:
            print("Test execution failed.")
            return

        # Load test results
        with open(test_report_path, 'r') as file:
            test_report = json.load(file)

        # Get tool versions
        tool_versions = get_tool_versions(container)

        # Generate Markdown report
        generate_markdown(test_report, tool_versions)

    finally:
        # Cleanup: Stop and remove container
        container.stop()
        container.remove()
        print(f"Container {container_name} stopped and removed.")

if __name__ == "__main__":
    main()
