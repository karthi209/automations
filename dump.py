import json
import collections
from datetime import datetime

def generate_mermaid_chart(results):
    """Generate a Mermaid chart showing test results distribution."""
    chart = ["```mermaid", "pie title Overall Test Results"]
    
    # Aggregate total passed and failed tests
    total_passed = sum(data['passed'] for data in results.values())
    total_tests = sum(data['total'] for data in results.values())
    total_failed = total_tests - total_passed
    
    # Add data points if there are any tests
    if total_tests > 0:
        passed_percentage = (total_passed / total_tests) * 100
        failed_percentage = (total_failed / total_tests) * 100
        
        chart.extend([
            f'    "Passed ({total_passed})" : {passed_percentage:.1f}',
            f'    "Failed ({total_failed})" : {failed_percentage:.1f}'
        ])
    
    chart.append("```")
    return "\n".join(chart)

def generate_tool_chart(results):
    """Generate a Mermaid bar chart showing per-tool results."""
    chart = [
        "```mermaid",
        "%%{init: {'theme': 'forest'}}%%",
        "gantt",
        "    title Test Results by Tool",
        "    dateFormat X",
        "    axisFormat %s",
        "    section Results"
    ]
    
    # Add a bar for each tool
    for tool, data in results.items():
        pass_rate = (data['passed'] / data['total']) * 100 if data['total'] > 0 else 0
        chart.append(f"    {tool} : 0, {pass_rate}")
    
    chart.append("```")
    return "\n".join(chart)

def format_failure_details(failures):
    """Format failure details as a collapsible section."""
    if not failures:
        return ""
    
    # Count total failures
    total_failures = len(failures)
    
    # Create collapsible section
    details = [f"\n### Failure Details ({total_failures} failures)\n"]
    details.append("<details>")
    details.append("<summary>Click to expand failure details</summary>\n")
    
    # Add each failure
    for failure in failures:
        details.extend([
            f"#### Test Case: {failure['tool']}",
            f"**Test Name:** {failure['test_name']}",
            "```plaintext",
            f"{failure['message']}",
            "```\n"
        ])
    
    details.append("</details>")
    return "\n".join(details)

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
            failure_message = test.get('call', {}).get('longrepr', 'No detailed message available')
            short_message = '\n'.join(failure_message.splitlines()[:5])
            failures.append({
                'tool': tool,
                'test_name': test['nodeid'],
                'message': short_message
            })
    
    # Generate markdown content
    markdown_content = "\n## Summary - Integration Tests\n\n"
    markdown_content += f"\n*Report for {filename}*\n\n"
    markdown_content += f"_Last updated: {current_time}_\n\n"
    
    # Add overall visualization
    markdown_content += "\n### Overall Test Results\n\n"
    markdown_content += generate_mermaid_chart(results)
    
    # Add per-tool visualization
    markdown_content += "\n\n### Results by Tool\n\n"
    markdown_content += generate_tool_chart(results)
    
    # Add detailed results table
    markdown_content += "\n\n### Detailed Results\n\n"
    markdown_content += "| Tool | Tests Passed | Final Health |\n"
    markdown_content += "|------|--------------|---------------|\n"
    
    # Add each tool's results
    for tool, counts in sorted(results.items()):
        passed_fraction = f"{counts['passed']}/{counts['total']}"
        health = "✅ HEALTHY" if counts['passed'] == counts['total'] else "❌ UNHEALTHY"
        markdown_content += f"| {tool} | {passed_fraction} | {health} |\n"
    
    # Add collapsible failure details
    markdown_content += format_failure_details(failures)
    
    return markdown_content

def append_markdown(content, filename="test_results.md"):
    with open(filename, 'a') as f:
        f.write(content)

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
        append_markdown(markdown_content)
        print(f"Markdown file updated successfully with results from {filename}!")
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
