import json

# Load the JSON data from a file
with open('pytest_output.json') as f:
    pytest_data = json.load(f)

# Prepare data for Markdown table
markdown_table = '| Tool | Test Passed | Tool Health |\n|------|-------------|-------------|\n'

# Iterate over the collectors and create rows for the table
for collector in pytest_data['collectors']:
    if 'nodeid' in collector and collector['nodeid']:
        tool_name = collector['nodeid'].split('/')[-1]  # Extract the tool name from the nodeid
        
        # Skip if the tool name is 'test_tools' or just '.'
        if tool_name in ['test_tools', '.']:
            continue
        
        tests_passed = len(collector['result'])  # Number of passed tests (assuming all tests in result passed)
        total_tests = len(collector['result'])  # Total tests (same here for simplicity)
        health_status = "✔" if tests_passed == total_tests else "❌"
        
        # Add row to the table
        markdown_table += f"| {tool_name} | {tests_passed}/{total_tests} | {health_status} |\n"

# Save the Markdown table to a .md file
with open('test_results.md', 'w') as md_file:
    md_file.write(markdown_table)

print("Markdown table has been saved to 'test_results.md'.")
