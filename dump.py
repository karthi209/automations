import subprocess
import os
import json
import docker

# Docker settings
DOCKER_IMAGE_NAME = "your-docker-image-name"  # This will be passed from the command line
CONTAINER_NAME = f"test_container_{os.urandom(4).hex()}"
TEST_REPORT_PATH = '/tmp/test_tools/test_report.json'
TOOL_VERSION_PATH = '/tmp/test_tools/tool_version.json'
OUTPUT_REPORT_PATH = '/tmp/test_tools/final_report.md'
TEST_FILES_DIR = '/path/to/test_files'  # Modify this with the correct path
TEST_CONTAINER_DIR = '/tmp/test_tools'

SUCCESS_ICON = "✅"
FAILURE_ICON = "❌"

def load_json(file_path):
    """Load a JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to parse {file_path}. Ensure it is valid JSON.")
        return {}

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

def run_tests(container):
    """Run pytest inside the container and generate a JSON report."""
    try:
        # Running the pytest command in the virtual environment inside the container
        command = f"source /tmp/test_tools/venv/bin/activate && pytest --json-report --json-report-file=/tmp/test_tools/test_report.json"
        result = container.exec_run(command)

        # Print the output of the pytest command to debug issues
        print("Pytest output:")
        print(result.output.decode())

        # Check if the test report was generated
        if result.exit_code != 0:
            print("Error: Pytest failed to run successfully.")
            return None
        return '/tmp/test_tools/test_report.json'

    except Exception as e:
        print(f"Error running tests: {e}")
        return None

def run_docker_container():
    """Start the Docker container, install dependencies, and run tests."""
    try:
        # Connect to Docker
        client = docker.from_env()

        # Create and start a Docker container
        container = client.containers.run(
            DOCKER_IMAGE_NAME,
            name=CONTAINER_NAME,
            detach=True,
            volumes={
                TEST_FILES_DIR: {'bind': TEST_CONTAINER_DIR, 'mode': 'rw'}
            },
            environment=["PYTHONPATH=/tmp/test_tools"],
        )

        print(f"Container {CONTAINER_NAME} started successfully.")

        # Set up a virtual environment inside the container
        container.exec_run("python3 -m venv /tmp/test_tools/venv")
        container.exec_run("source /tmp/test_tools/venv/bin/activate && pip install pytest")

        # Run tests inside the container
        test_report_path = run_tests(container)

        if test_report_path:
            print(f"Test report saved to {test_report_path}")
        else:
            print("Error: Test report was not generated.")
            return

        # After tests are done, copy the test report and tool versions from the container to the host
        with open(TEST_REPORT_PATH, 'wb') as f:
            f.write(container.exec_run(f"cat {test_report_path}").output)

        # Assuming tool versions are saved to TOOL_VERSION_PATH, copy them
        with open(TOOL_VERSION_PATH, 'wb') as f:
            f.write(container.exec_run(f"cat {TOOL_VERSION_PATH}").output)

        # Generate the final markdown report
        test_report = load_json(TEST_REPORT_PATH)
        tool_versions = load_json(TOOL_VERSION_PATH)

        if test_report and tool_versions:
            generate_markdown(test_report, tool_versions)

        # Clean up: Stop and remove the container after tests
        container.stop()
        container.remove()

    except docker.errors.DockerException as e:
        print(f"Error: Docker-related issue: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_docker_container()
