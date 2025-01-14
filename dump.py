import json


def parse_test_report(report_file):
    """
    Parses the pytest JSON report and generates a Markdown summary with tool names,
    their version, the results for the tests, and tool health.

    :param report_file: Path to the pytest JSON report.
    :return: Markdown formatted report.
    """
    try:
        with open(report_file, "r") as file:
            report_data = json.load(file)

        tools_results = []

        # Iterate through tests to process results for each tool
        for test in report_data.get("tests", []):
            test_name = test.get("nodeid", "Unknown Test")
            outcome = test.get("outcome", "unknown")
            message = test.get("message", "")

            # Extract the tool name from the test name (assuming tool names are part of the test nodeid)
            tool_name = test_name.split("::")[0]  # Use the first part of the test name as tool name

            # Extract the version from the test message
            version = None
            if "version:" in message:
                version = message.split("version:")[-1].strip()

            # Prepare outcome symbols for pass/fail
            outcome_symbol = "✅" if outcome == "passed" else "❌" if outcome == "failed" else "⏸️"

            # Store results for the tool in the form of (tool_name, version, number of passed tests, total tests)
            tool_result = next((tool for tool in tools_results if tool["tool_name"] == tool_name), None)
            if tool_result is None:
                tool_result = {
                    "tool_name": tool_name,
                    "version": version,
                    "passed_tests": 0,
                    "total_tests": 0,
                }
                tools_results.append(tool_result)

            # Increment the number of tests for this tool
            tool_result["total_tests"] += 1
            if outcome == "passed":
                tool_result["passed_tests"] += 1

        # Start creating the markdown report
        markdown_report = f"## Test Results Summary\n\n"
        markdown_report += "| Tool Name | Tool Version | Test Results | Tool Health |\n"
        markdown_report += "|-----------|--------------|--------------|-------------|\n"

        # Add rows for each tool's result
        for tool_result in tools_results:
            test_results = f"{tool_result['passed_tests']}/{tool_result['total_tests']}"
            version = tool_result["version"] if tool_result["version"] else "N/A"
            
            # Determine the tool health based on test results
            tool_health = "✅" if tool_result["passed_tests"] == tool_result["total_tests"] else "❌"
            
            markdown_report += f"| {tool_result['tool_name']} | {version} | {test_results} | {tool_health} |\n"

        return markdown_report

    except FileNotFoundError:
        return f"Error: The file {report_file} does not exist."
    except json.JSONDecodeError:
        return f"Error: The file {report_file} is not a valid JSON file."


def write_markdown(report_file, output_file):
    """
    Processes the pytest JSON report and writes it to a Markdown file.

    :param report_file: Path to the pytest JSON report.
    :param output_file: Path to the output Markdown file.
    """
    markdown_report = parse_test_report(report_file)
    with open(output_file, "w") as file:
        file.write(markdown_report)
    print(f"Markdown report written to {output_file}")


if __name__ == "__main__":
    # Paths to the input JSON file and the output Markdown file
    report_file = "test_report.json"  # pytest JSON report
    output_file = "test_report.md"    # Output Markdown file

    # Generate the Markdown report
    write_markdown(report_file, output_file)
