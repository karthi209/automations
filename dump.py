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

def get_tool_name_from_nodeid(nodeid):
    """Extract tool name from the test nodeid."""
    try:
        # Ensure nodeid contains the expected format
        if nodeid:
            # Assuming the tool name is the part of the filename before the first period (e.g., 'git' from 'test_git.py')
            tool_name = nodeid.split('/')[1].split('.')[0]
            return tool_name
        else:
            return None
    except IndexError:
        return None

def generate_markdown_report(test_report, tool_version_report):
    """Generate a Markdown report combining the test results and tool versions."""
    tools_status = {}
    
    # Loop through test results and gather the outcomes
    for collector in test_report['collectors']:
        if collector['nodeid']:
            # Extract the tool name (assumed from the test file name)
            tool_name = get_tool_name_from_nodeid(collector['nodeid'])
            
            if tool_name:  # Only proceed if a valid tool name was found
                # Initialize tool status if not already
                if tool_name not in tools_status:
                    # Get version from the tool_version_report
                    tool_version = tool_version_report.get(tool_name, 'Version not found')
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
    # Load the test report and tool version report
    test_report = load_json_file(TEST_REPORT_PATH)
    tool_version_report = load_json_file(TOOL_VERSION_PATH)

    # Generate the final Markdown report
    generate_markdown_report(test_report, tool_version_report)
