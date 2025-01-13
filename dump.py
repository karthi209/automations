import subprocess
import json
import os
import sys
import time

DOCKER_OUTPUT_FILE = "/output/test_results.json"
HOST_OUTPUT_FILE = "test_results.json"
EXPECTED_VALUES_FILE = "expected_values.json"

def run_docker_tests(image_name, test_scripts, expected_values_file):
    """Run all tests inside a Docker container."""
    # Generate a unique container name
    container_name = f"test-container-{int(time.time())}"
    
    try:
        # Pull the Docker image
        print(f"Pulling Docker image {image_name}...")
        subprocess.check_call(["docker", "pull", image_name])
        
        # Start the container
        print(f"Starting Docker container {container_name}...")
        subprocess.check_call([
            "docker", "run", "-d", "--name", container_name, image_name, "tail", "-f", "/dev/null"
        ])
        
        # Copy test scripts and the source of truth file into the container
        print("Copying test files into the container...")
        os.makedirs("output", exist_ok=True)  # Ensure output directory exists
        for script in test_scripts:
            subprocess.check_call(["docker", "cp", script, f"{container_name}:/test_tools/"])
        subprocess.check_call(["docker", "cp", expected_values_file, f"{container_name}:/test_tools/"])

        # Run the test manager script inside the container
        print("Running tests inside the Docker container...")
        subprocess.check_call([
            "docker", "exec", container_name, "python3", "/test_tools/test_tools.py"
        ])

        # Copy the results back to the host
        print("Copying results back to the host...")
        subprocess.check_call([
            "docker", "cp", f"{container_name}:{DOCKER_OUTPUT_FILE}", HOST_OUTPUT_FILE
        ])

        print(f"Tests completed. Results saved to {HOST_OUTPUT_FILE}.")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    finally:
        # Stop and remove the container
        print(f"Stopping and removing container {container_name}...")
        subprocess.call(["docker", "stop", container_name])
        subprocess.call(["docker", "rm", container_name])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test_manager.py <docker_image_name>")
        sys.exit(1)

    image_name = sys.argv[1]  # Docker image name
    test_scripts = [
        "test_tools/test_python3.py",
        "test_tools/test_maven.py",
        "test_tools/test_curl.py",
        "test_tools/test_tools.py"
    ]
    expected_values_file = EXPECTED_VALUES_FILE

    run_docker_tests(image_name, test_scripts, expected_values_file)





import subprocess
import json
import os

OUTPUT_FILE = "/output/test_results.json"
EXPECTED_VALUES_FILE = "/test_tools/expected_values.json"

def load_expected_values():
    """Load expected values from the source of truth JSON file."""
    try:
        with open(EXPECTED_VALUES_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading expected values: {e}")
        return {}

def write_results_to_file(results):
    """Write test results to a JSON file."""
    os.makedirs("/output", exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=4)

def run_individual_tests(test_scripts):
    """Run individual tool tests and consolidate results."""
    results = {}
    expected_values = load_expected_values()

    for script in test_scripts:
        tool_name = os.path.basename(script).replace("test_", "").replace(".py", "").capitalize()
        print(f"Running tests for {tool_name}...")
        try:
            output = subprocess.check_output(["python3", script]).decode("utf-8")
            tool_results = json.loads(output)

            # Compare results with expected values
            comparison = compare_results_with_expected(tool_name, tool_results, expected_values)
            results[tool_name] = {
                "Results": tool_results,
                "Comparison": comparison
            }
        except Exception as e:
            results[tool_name] = {"Error": str(e)}

    return results

def compare_results_with_expected(tool_name, results, expected_values):
    """Compare actual results with expected values."""
    comparison = {}
    if tool_name in expected_values:
        expected = expected_values[tool_name]
        for key, value in results.items():
            expected_key = f"Expected {key}"
            if expected_key in expected:
                comparison[key] = {
                    "Actual": value,
                    "Expected": expected[expected_key],
                    "Match": value == expected[expected_key]
                }
            else:
                comparison[key] = {
                    "Actual": value,
                    "Expected": "Not defined in source of truth",
                    "Match": "Unknown"
                }
    else:
        comparison["Error"] = f"No expected values defined for {tool_name}"
    return comparison

if __name__ == "__main__":
    test_scripts = [
        "/test_tools/test_python3.py",
        "/test_tools/test_maven.py",
        "/test_tools/test_curl.py",
    ]
    results = run_individual_tests(test_scripts)
    write_results_to_file(results)
