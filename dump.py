import json
import collections

def process_test_results(json_data):
    # Parse the JSON data
    data = json.loads(json_data)
    
    # Create a dictionary to store results for each tool
    results = collections.defaultdict(lambda: {'passed': 0, 'total': 0})
    
    # Process each test result
    for test in data['tests']:
        # Extract tool name from test path
        tool = test['nodeid'].split('/')[1].split('_')[1].split('.')[0]
        
        # Count passed tests and total tests
        results[tool]['total'] += 1
        if test['outcome'] == 'passed':
            results[tool]['passed'] += 1
    
    # Generate markdown content
    markdown_content = "# Test Results Summary\n\n"
    markdown_content += "| Tool | Tests Passed | Final Health |\n"
    markdown_content += "|------|--------------|---------------|\n"
    
    # Add each tool's results
    for tool, counts in results.items():
        passed_fraction = f"{counts['passed']}/{counts['total']}"
        health = "✅ HEALTHY" if counts['passed'] == counts['total'] else "❌ UNHEALTHY"
        
        markdown_content += f"| {tool.capitalize()} | {passed_fraction} | {health} |\n"
    
    return markdown_content

def save_markdown(content, filename="test_results.md"):
    with open(filename, 'w') as f:
        f.write(content)

# Example usage
if __name__ == "__main__":
    # Read the input file
    with open('paste.txt', 'r') as f:
        json_data = f.read()
    
    # Process and generate markdown
    markdown_content = process_test_results(json_data)
    
    # Save to file
    save_markdown(markdown_content)
    print("Markdown file generated successfully!")
