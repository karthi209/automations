import json

# Paths to the reports
TEST_REPORT_PATH = 'test_report.json'
TOOL_VERSION_PATH = 'tool_version.json'
OUTPUT_REPORT_PATH = 'final_report.md'

# Icons for success and failure
SUCCESS_ICON = "✅"
FAILURE_ICON = "❌"

def load_json_file(file_path):
    """Helper function to load a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to parse {file_path}. Ensure it's valid JSON.")
        return {}

def generate_markdown_report(test_report, tool_version_report, tool_test_mapping):
    """Generate a Markdown report combining the test results and tool versions."""
    tools_status = {}
    
    # Loop through test results and gather the outcomes
    for collector in test_report.get('collectors', []):
        nodeid = collector.get('nodeid', "")
        
        # Ensure nodeid is not empty and has the expected format
        if nodeid and '/' in nodeid:
            # Extract the test file name from nodeid
            test_file_name = nodeid.split('/')[1].split('.')[0]
            
            # Lookup the tool name from the predefined mapping
            tool_name = tool_test_mapping.get(test_file_name)
            
            if tool_name:
                # Get version from the tool_version_report
                tool_version = tool_version_report.get(tool_name, 'Version not found')

                # Initialize tool status if not already present
                if tool_name not in tools_status:
                    tools_status[tool_name] = {
                        'version': tool_version,
                        'tests': []
                    }
                
                # Add each test result to the tool's record
                for test in collector.get('result', []):
                    nodeid = test.get('nodeid', "")
                    if '::' in nodeid:
                        test_name = nodeid.split('::')[1]
                    else:
                        test_name = "Unknown Test"
                    
                    test_outcome = collector.get('outcome', "unknown")
                    status_icon = SUCCESS_ICON if test_outcome == 'passed' else FAILURE_ICON
                    tools_status[tool_name]['tests'].append({
                        'test_name': test_name,
                        'outcome': test_outcome,
                        'icon': status_icon
                    })
        else:
            print(f"Warning: Unexpected nodeid format: {nodeid}")

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
