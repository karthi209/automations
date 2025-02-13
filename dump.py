import json
import collections
from datetime import datetime

def process_test_results(json_data):
    # Parse the JSON data
    data = json.loads(json_data)
    
    # Create dictionaries to store results for each tool and failure details
    results = collections.defaultdict(lambda: {'passed': 0, 'total': 0})
    failures = []

    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    # Process each test result
    for test in data['tests']:
        # Extract tool name from test path
        tool = test['nodeid'].split('/')[1].split('_')[1].split('.')[0]
        
        # Count passed tests and total tests
        results[tool]['total'] += 1
        if test['outcome'] == 'passed':
            results[tool]['passed'] += 1
        else:
            # Add failure details
            failures.append({
                'tool': tool,
                'test_name': test['nodeid'],
                'message': test.get('call', {}).get('longrepr', 'No detailed message available')
            })
    
    # Generate markdown content
    markdown_content = "## Summary - Integration Tests\n\n"
    markdown_content += f"_Last updated: {current_time}_\n\n"
    markdown_content += "| Tool | Tests Passed | Final Health |\n"
    markdown_content += "|------|--------------|---------------|\n"
    
    # Add each tool's results
    for tool, counts in results.items():
        passed_fraction = f"{counts['passed']}/{counts['total']}"
        health = "✅ HEALTHY" if counts['passed'] == counts['total'] else "❌ UNHEALTHY"
        
        markdown_content += f"| {tool} | {passed_fraction} | {health} |\n"
    
    # Add failure details, if any
    if failures:
        markdown_content += "\n## Failure Details\n\n"
        for failure in failures:
            markdown_content += f"### Test Case: {failure['tool']}\n"
            markdown_content += f"**Test Name:** {failure['test_name']}\n"
            markdown_content += "```plaintext\n"
            markdown_content += f"{failure['message']}\n"
            markdown_content += "```\n\n"
    
    return markdown_content

def save_markdown(content, filename="test_results.md"):
    with open(filename, 'w') as f:
        f.write(content)

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python script.py <test_report.json>")
        sys.exit(1)

    filename = sys.argv[1]  # Take file name as input

    try:
        with open(filename, 'r') as f:
            json_data = f.read()
        
        markdown_content = process_test_results(json_data)
        save_markdown(markdown_content)

        print(f"Markdown file generated successfully from {filename}!")
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
