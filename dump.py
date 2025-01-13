import subprocess
import os
import sys
import time

DOCKER_OUTPUT_FILE = "/output/test_results.json"
HOST_OUTPUT_FILE = "test_results.json"
EXPECTED_VALUES_FILE = "expected_values.json"

def run_docker_tests(image_name):
    """Run tests inside a Docker container."""
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
        
        # Copy the test folder and source of truth JSON into the container
        print("Copying test files into the container...")
        subprocess.check_call(["docker", "cp", "test_tools", f"{container_name}:/test_tools"])
        subprocess.check_call(["docker", "cp", EXPECTED_VALUES_FILE, f"{container_name}:/test_tools/"])

        # Run the master test script inside the container
        print("Running tests inside the Docker container...")
        subprocess.check_call([
            "docker", "exec", container_name, "python3", "/test_tools/run_tests.py"
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
    run_docker_tests(image_name)




import os
import json
import subprocess

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

def run_test_script(script_path):
    """Run an individual test script and return its output."""
    try:
        output = subprocess.check_output(["python3", script_path]).decode("utf-8")
        return json.loads(output)
    except Exception as e:
        return {"Error": str(e)}

def compare_results_with_expected(tool_name, results, expected_values):
    """Compare actual results with expected values."""
    comparison = {}
    if tool_name in expected_values:
        expected = expected_values[tool_name]
        for key, value in results.items():
            expected_key = f"Expected {key}"
            comparison[key] = {
                "Actual": value,
                "Expected": expected.get(expected_key, "Not defined"),
                "Match": value == expected.get(expected_key)
            }
    else:
        comparison["Error"] = "No expected values defined for this tool"
    return comparison

def main():
    """Run all tool tests and generate a consolidated report."""
    expected_values = load_expected_values()
    results = {}
    
    # Run each tool test script in the `test_tools` directory
    for script in os.listdir("/test_tools"):
        if script.startswith("test_") and script.endswith(".py") and script != "run_tests.py":
            tool_name = script.replace("test_", "").replace(".py", "").capitalize()
            print(f"Testing {tool_name}...")
            tool_results = run_test_script(f"/test_tools/{script}")
            comparison = compare_results_with_expected(tool_name, tool_results, expected_values)
            results[tool_name] = {
                "Results": tool_results,
                "Comparison": comparison
            }

    # Write results to the output file
    os.makedirs("/output", exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    main()



{
    "Python3": {
        "Expected Version": "3.8.10",
        "Expected Installation Path": "/usr/bin/python3",
        "Expected Symlink": "python3 -> /usr/bin/python3.8"
    },
    "Maven": {
        "Expected Version": "3.6.3",
        "Expected Installation Path": "/usr/bin/mvn",
        "Expected Symlink": "mvn -> /usr/share/maven/bin/mvn"
    }
}



import subprocess
import json

def main():
    try:
        version = subprocess.check_output(["python3", "--version"]).decode("utf-8").strip()
        path = subprocess.check_output(["which", "python3"]).decode("utf-8").strip()
        symlink = subprocess.check_output(["ls", "-l", path]).decode("utf-8").strip()
        
        # Functionality test
        functionality_test = subprocess.check_output(["python3", "-c", "print('Hello, World!')"]).decode("utf-8").strip()
        
        results = {
            "Version": version.split()[1],
            "Installation Path": path,
            "Symlink": symlink,
            "Functionality Test": functionality_test
        }
    except Exception as e:
        results = {"Error": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    main()
