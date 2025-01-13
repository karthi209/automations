import subprocess
import json
import os
import time

OUTPUT_FILE = "test_results.json"
EXPECTED_VALUES_FILE = "expected_values.json"

def load_expected_values(file_path):
    """Load expected values from the source of truth JSON file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading expected values: {e}")
        return {}

def write_results_to_file(results):
    """Save the consolidated test results to a JSON file."""
    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=4)

def run_tool_tests(tools):
    """Run test scripts for each tool and consolidate results."""
    results = {}
    expected_values = load_expected_values(EXPECTED_VALUES_FILE)

    for tool_name, script_path in tools.items():
        print(f"Running tests for {tool_name}...")
        try:
            output = subprocess.check_output(["python3", script_path]).decode("utf-8")
            tool_results = json.loads(output)

            # Compare with expected values
            comparison = compare_results_with_expected(tool_name, tool_results, expected_values)
            results[tool_name] = {
                "Results": tool_results,
                "Comparison": comparison
            }
        except Exception as e:
            print(f"Error testing {tool_name}: {e}")
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
    # Define tool test scripts
    tools = {
        "Python3": "test_tools/test_python3.py",
        "Maven": "test_tools/test_maven.py",
        "Curl": "test_tools/test_curl.py",
    }

    print("Running all tool tests...")
    results = run_tool_tests(tools)

    print(f"Saving results to {OUTPUT_FILE}...")
    write_results_to_file(results)

    print(f"All tests completed. Results saved to {OUTPUT_FILE}.")




import subprocess
import json

def test_python3():
    results = {}
    try:
        # Test Version
        version = subprocess.check_output(["python3", "--version"]).decode("utf-8").strip().split(" ")[1]
        results["Version"] = version
    except Exception as e:
        results["Version"] = f"Error: {e}"

    try:
        # Test Installation Path
        install_path = subprocess.check_output(["which", "python3"]).decode("utf-8").strip()
        results["Installation Path"] = install_path
    except Exception as e:
        results["Installation Path"] = f"Error: {e}"

    try:
        # Test Symlink Path
        symlink = subprocess.check_output(["ls", "-l", "/usr/bin/python3"]).decode("utf-8").strip()
        results["Symlink"] = symlink
    except Exception as e:
        results["Symlink"] = "Not present or Error: " + str(e)

    return results

if __name__ == "__main__":
    results = test_python3()
    print(json.dumps(results))




import subprocess
import json

def test_maven():
    results = {}
    try:
        # Test Version
        version = subprocess.check_output(["mvn", "--version"]).decode("utf-8").strip().split("\n")[0]
        results["Version"] = version.split(" ")[-1]
    except Exception as e:
        results["Version"] = f"Error: {e}"

    try:
        # Test Installation Path
        install_path = subprocess.check_output(["which", "mvn"]).decode("utf-8").strip()
        results["Installation Path"] = install_path
    except Exception as e:
        results["Installation Path"] = f"Error: {e}"

    try:
        # Test Symlink Path
        symlink = subprocess.check_output(["ls", "-l", "/usr/bin/mvn"]).decode("utf-8").strip()
        results["Symlink"] = symlink
    except Exception as e:
        results["Symlink"] = "Not present or Error: " + str(e)

    return results

if __name__ == "__main__":
    results = test_maven()
    print(json.dumps(results))
