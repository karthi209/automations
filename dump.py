import json
import os

# Paths to the input JSON files
TEST_REPORT_FILE = 'test_report.json'
TOOL_VERSIONS_FILE = 'tool_versions.json'

# Path to the output Markdown file
OUTPUT_MD_FILE = 'test_summary.md'

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

def generate_test_results_section(test_report):
    """Generate a Markdown section for test results."""
    if not test_report:
        return "### Test Results\nNo test results available.\n"
    
    section = "### Test Results\n\n"
    
    # Extract relevant information from the JSON test report
    summary = test_report.get("summary", {})
    total_tests = summary.get("total", 0)
    passed_tests = summary.get("passed", 0)
    failed_tests = summary.get("failed", 0)
    skipped_tests = summary.get("skipped", 0)
    
    section += f"- **Total Tests**: {total_tests}\n"
    section += f"- **Passed**: {passed_tests}\n"
    section += f"- **Failed**: {failed_tests}\n"
    section += f"- **Skipped**: {skipped_tests}\n"
    
    # List of failed tests, if any
    if failed_tests > 0:
        section += "\n#### Failed Tests\n"
        for test in test_report.get("tests", []):
            if test.get("outcome") == "failed":
                section += f"- {test.get('test', 'Unknown Test')}: {test.get('message', 'No message')}\n"
    
    section += "\n"
    return section

def generate_markdown_report(test_report, tool_versions):
    """Generate the full Markdown report combining test results and tool versions."""
    report = "# Test Summary Report\n\n"
    
    # Generate the sections
    report += generate_tool_versions_section(tool_versions)
    report += generate_test_results_section(test_report)
    
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
