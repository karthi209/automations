import subprocess
import json
import os

def load_expected_values(file_path):
    """Load expected values from the source of truth JSON file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading expected values: {e}")
        return {}


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


def write_results_to_file(tool_name, results, comparison, output_file="test_results.json"):
    """Save the test results and comparisons to a JSON file."""
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            all_results = json.load(f)
    else:
        all_results = {}

    all_results[tool_name] = {
        "Results": results,
        "Comparison": comparison
    }

    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=4)


def test_python3():
    """Test details for Python3."""
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
    tool_name = "Python3"
    output_file = "test_results.json"
    expected_values_file = "expected_values.json"

    print(f"Loading expected values from {expected_values_file}...")
    expected_values = load_expected_values(expected_values_file)

    print(f"Running tests for {tool_name}...")
    results = test_python3()

    print("Comparing results with expected values...")
    comparison = compare_results_with_expected(tool_name, results, expected_values)

    print(f"Saving results to {output_file}...")
    write_results_to_file(tool_name, results, comparison, output_file)

    print(f"Results saved for {tool_name}.")



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
