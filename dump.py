import json
import os

# Paths to the input JSON files
TEST_REPORT_DIR = 'tools_test'  # Directory containing individual test result JSON files
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

def load_tool_versions():
    """Load tool versions from the JSON config."""
    tool_versions = load_json(TOOL_VERSIONS_FILE)
    if not tool_versions:
        return {}
    return tool_versions

def generate_tool_versions_section(tool_versions):
    """Generate a Markdown section for tool versions."""
    if not tool_versions:
        return "### Tool Versions\nNo tool version data available.\n"
    
    section = "### Tool Versions\n\n"
    for tool, version in tool_versions.items():
        section += f"- **{tool}**: {version}\n"
    section += "\n"
    return section

def extract_tool_name_from_filename(filename):
    """Extract the tool name from the filename (e.g., 'test_git' -> 'git')."""
    return filename.split('_')[1] if '_' in filename else filename

def generate_test_results_section(test_reports, tool_versions):
    """Generate a Markdown section for categorized test results."""
    if not test_reports:
        return "### Test Results\nNo test results available.\n"
    
    section = "### Test Results by Tool\n\n"
    
    for tool, tests in test_reports.items():
        version = tool_versions.get(tool, "Version not found")
        section += f"#### {tool} (Version: {version})\n"
        
        for test in tests:
            outcome = test["outcome"]
            icon = SUCCESS_ICON if outcome == "passed" else FAILURE_ICON
            section += f"- {icon} **{test['name']}**: {test['message']}\n"
        section += "\n"
    
    return section

def categorize_tests_by_tool():
    """Categorize test results by tool based on the filenames."""
    test_reports = {}
    
    for filename in os.listdir(TEST_REPORT_DIR):
        if filename.endswith('.json'):
            tool_name = extract_tool_name_from_filename(filename)
            file_path = os.path.join(TEST_REPORT_DIR, filename)
            
            # Load the test report for this tool
            test_report = load_json(file_path)
            if not test_report:
                continue
            
            if tool_name not in test_reports:
                test_reports[tool_name] = []
            
            # Add the test results to the categorized list
            for test in test_report.get("tests", []):
                test_reports[tool_name].append({
                    "name": test.get('test', 'Unnamed Test'),
                    "outcome": test.get('outcome', 'unknown'),
                    "message": test.get('message', 'No message')
                })
    
    return test_reports

def generate_markdown_report(test_reports, tool_versions):
    """Generate the full Markdown report combining test results and tool versions."""
    report = "# Test Summary Report\n\n"
    
    # Generate the sections
    report += generate_tool_versions_section(tool_versions)
    
    # Generate the test results section
    report += generate_test_results_section(test_reports, tool_versions)
    
    return report

def save_report(report, output_file):
    """Save the generated Markdown report to a file."""
    with open(output_file, 'w') as f:
        f.write(report)
    print(f"Markdown report saved to {output_file}")

def main():
    # Load the tool versions data
    tool_versions = load_tool_versions()
    if not tool_versions:
        print("Error: Tool versions data is missing or invalid.")
        return
    
    # Categorize the tests by tool based on filenames
    test_reports = categorize_tests_by_tool()
    if not test_reports:
        print("Error: Test reports are missing or invalid.")
        return
    
    # Generate the Markdown report
    report = generate_markdown_report(test_reports, tool_versions)
    
    # Save the report to a file
    save_report(report, OUTPUT_MD_FILE)

if __name__ == "__main__":
    main()
