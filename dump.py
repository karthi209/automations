import json
import os

# Paths to the reports
TEST_REPORT_PATH = 'test_report.json'
TOOL_VERSION_PATH = 'tool_version.json'
OUTPUT_REPORT_PATH = 'final_report.md'

# Icons for success and failure
SUCCESS_ICON = "✅"
FAILURE_ICON = "❌"

def load_json_file(file_path):
    """Helper function to load a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def generate_markdown_report(test_report, tool_version_report, tool_test_mapping):
    """Generate a Markdown report combining the test results and tool versions."""
    tools_status = {}
    
    # Loop through test results and gather the outcomes
    for collector in test_report['collectors']:
        if collector['nodeid']:
            # Extract the tool name based on the test file name (from tool_test_mapping)
            test_file_name = collector['nodeid'].split('/')[1].split('.')[0]
            
            # Lookup the tool name from the predefined mapping
            tool_name = tool_test_mapping.get(test_file_name, None)
            
            if tool_name:  # Only proceed if a valid tool name was found
                print(f"Tool: {tool_name} (from {test_file_name})")  # Log the tool name

                # Get version from the tool_version_report
                if tool_name in tool_version_report:
                    tool_version = tool_version_report[tool_name]
                else:
                    tool_version = 'Version not found'
                    print(f"Tool version not found for: {tool_name}")  # Log if version is not found
                
                # Initialize tool status if not already
                if tool_name not in tools_status:
                    tools_status[tool_name] = {
                        'version': tool_version,
                        'tests': []
                    }
                
                # Add each test result to the tool's record
                for test in collector['result']:
                    test_outcome = collector['outcome']
                    status_icon = SUCCESS_ICON if test_outcome == 'passed' else FAILURE_ICON
                    tools_status[tool_name]['tests'].append({
                        'test_name': test['nodeid'].split('::')[1],
                        'outcome': test_outcome,
                        'icon': status_icon
                    })
    
    # Generate the Markdown report
    markdown_report = "# Test Summary Report\n\n"
    
    for tool, data in tools_status.items():
        markdown_report += f"## {tool} (Version: {data['version']})\n"
        for test in data['tests']:
            markdown_report += f"- {test['test_name']} : {test['icon']} ({test['outcome']})\n"
        markdown_report += "\n"
    
    # Save the report to a Markdown file
    with open(OUTPUT_REPORT_PATH, 'w') as f:
        f.write(markdown_report)

    print(f"Report saved to {OUTPUT_REPORT_PATH}")

if __name__ == '__main__':
    # Define the mapping of test files to tool names
    tool_test_mapping = {
        "test_git": "git",
        "test_maven": "maven",
        # Add other test files to tool names as needed
    }

    # Load the test report and tool version report
    test_report = load_json_file(TEST_REPORT_PATH)
    tool_version_report = load_json_file(TOOL_VERSION_PATH)

    # Generate the final Markdown report
    generate_markdown_report(test_report, tool_version_report, tool_test_mapping)
