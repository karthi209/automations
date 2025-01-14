import json
import os

# Paths to the input JSON files
TEST_REPORT_FILE = 'test_report.json'
TOOL_VERSIONS_FILE = 'tool_versions.json'

# Path to the output Markdown file
OUTPUT_MD_FILE = 'test_summary.md'

# Icons for success and failure
SUCCESS_ICON = "✅"
FAILURE_ICON = "❌"

def load_json(file_path):
    """Load a JSON file and return its content."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} file not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to parse {file_path}, invalid JSON.")
        return None

def generate_tool_versions_section(tool_versions):
    """Generate a Markdown section for tool versions."""
    if not tool_versions:
        return "### Tool Versions\nNo tool version data available.\n"
    
    section = "### Tool Versions\n\n"
    for tool, version in tool_versions.items():
        section += f"- **{tool}**: {version}\n"
    section += "\n"
    return section

def categorize_tests_by_tool(test_report):
    """Categorize the tests by the tool name."""
    categorized_tests = {}

    # Extract relevant information from the JSON test report
    for test in test_report.get("tests", []):
        tool = test.get('tool', 'Unknown')
        outcome = test.get('outcome', 'unknown')
        test_name = test.get('test', 'Unnamed Test')
        message = test.get('message', 'No message')

        if tool not in categorized_tests:
            categorized_tests[tool] = []

        categorized_tests[tool].append({
            "name": test_name,
            "outcome": outcome,
            "message": message
        })
    
    return categorized_tests

def generate_test_results_section(categorized_tests):
    """Generate a Markdown section for categorized test results."""
    if not categorized_tests:
        return "### Test Results\nNo test results available.\n"
    
    section = "### Test Results by Tool\n\n"
    
    for tool, tests in categorized_tests.items():
        section += f"#### {tool}\n"
        for test in tests:
            outcome = test["outcome"]
            icon = SUCCESS_ICON if outcome == "passed" else FAILURE_ICON
            section += f"- {icon} **{test['name']}**: {test['message']}\n"
        section += "\n"
    
    return section

def generate_markdown_report(test_report, tool_versions):
    """Generate the full Markdown report combining test results and tool versions."""
    report = "# Test Summary Report\n\n"
    
    # Generate the sections
    report += generate_tool_versions_section(tool_versions)
    
    # Categorize tests by tool and generate the test results section
    categorized_tests = categorize_tests_by_tool(test_report)
    report += generate_test_results_section(categorized_tests)
    
    return report

def save_report(report, output_file):
    """Save the generated Markdown report to a file."""
    with open(output_file, 'w') as f:
        f.write(report)
    print(f"Markdown report saved to {output_file}")

def main():
    # Load the test report and tool versions data
    test_report = load_json(TEST_REPORT_FILE)
    tool_versions = load_json(TOOL_VERSIONS_FILE)
    
    if test_report is None or tool_versions is None:
        print("Error: Unable to generate the report due to missing or invalid data.")
        return
    
    # Generate the Markdown report
    report = generate_markdown_report(test_report, tool_versions)
    
    # Save the report to a file
    save_report(report, OUTPUT_MD_FILE)

if __name__ == "__main__":
    main()
