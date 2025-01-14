import json
import subprocess
import os
import docker
from pathlib import Path

# File paths
TOOL_VERSION_PATH = 'tool_version.json'
OUTPUT_REPORT_PATH = 'final_report.md'
TEST_DIR = Path("/tmp/test_tools")
SUCCESS_ICON = "✅"
FAILURE_ICON = "❌"

def spin_up_container(image_name, container_name, test_files):
    """Spin up a Docker container, copy test files, and run setup commands."""
    client = docker.from_env()
    try:
        # Create and start the container
        container = client.containers.run(
            image=image_name,
            name=container_name,
            command="sleep 300",
            detach=True,
            tty=True
        )
        print(f"Container {container_name} started.")

        # Copy test files
        for test_file in test_files:
            container.put_archive(
                TEST_DIR.as_posix(),
                Path(test_file).read_bytes()
            )
        print(f"Test files copied to {container_name}.")

        # Run setup commands
        container.exec_run("pip install pytest pytest-json-report")
        print("Dependencies installed.")
        return container

    except Exception as e:
        print(f"Error spinning up container: {e}")
        return None

def run_tests(container, json_report_path):
    """Run pytest inside the container and generate a JSON report."""
    try:
        result = container.exec_run(f"pytest --json-report --json-report-file={json_report_path}")
        print(result.output.decode())
        return json_report_path
    except Exception as e:
        print(f"Error running tests: {e}")
        return None

def get_tool_versions(container, tools):
    """Get the version of each tool inside the container."""
    versions = {}
    for tool in tools:
        try:
            result = container.exec_run(f"{tool} --version")
            output = result.output.decode().strip()
            versions[tool] = output.split()[1] if output else "Unknown version"
        except Exception as e:
            versions[tool] = "Error retrieving version"
            print(f"Error getting version for {tool}: {e}")
    return versions

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
    image_name = "your_image_name_here"
    container_name = "test_container"
    test_files = ["path_to_test_file_1", "path_to_test_file_2"]
    tools = ["git", "python", "node", "docker"]

    # Step 1: Spin up Docker container
    container = spin_up_container(image_name, container_name, test_files)
    if not container:
        print("Failed to create container.")
        return

    try:
        # Step 2: Run tests
        json_report_path = "/tmp/test_tools/.report.json"
        test_report = run_tests(container, json_report_path)

        # Step 3: Get tool versions
        tool_versions = get_tool_versions(container, tools)

        # Step 4: Generate Markdown report
        generate_markdown(test_report, tool_versions)

    finally:
        # Cleanup: Stop and remove the container
        container.stop()
        container.remove()
        print(f"Container {container_name} stopped and removed.")

if __name__ == "__main__":
    main()
