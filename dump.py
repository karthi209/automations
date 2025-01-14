import json

def parse_test_report(report_file):
    """
    Parses the pytest default JSON report and generates a Markdown summary.

    :param report_file: Path to the pytest JSON report.
    :return: Markdown formatted report.
    """
    try:
        with open(report_file, "r") as file:
            report_data = json.load(file)

        summary = report_data.get("summary", {})
        total_tests = summary.get("total", 0)
        passed_tests = summary.get("passed", 0)
        failed_tests = summary.get("failed", 0)
        skipped_tests = summary.get("skipped", 0)

        # Start creating the markdown report
        markdown_report = f"## Test Results Summary\n\n"
        markdown_report += f"Total Tests: {total_tests}\n"
        markdown_report += f"Passed: {passed_tests} ✅\n"
        markdown_report += f"Failed: {failed_tests} ❌\n"
        markdown_report += f"Skipped: {skipped_tests} ⏸️\n\n"

        markdown_report += "### Detailed Test Results\n\n"
        markdown_report += "| Test Name | Outcome | Duration | Message |\n"
        markdown_report += "|-----------|---------|----------|---------|\n"

        # Add each test result to the markdown table
        for test in report_data.get("tests", []):
            test_name = test.get("nodeid", "Unknown Test")
            outcome = test.get("outcome", "unknown")
            duration = test.get("duration", 0)
            message = test.get("message", "")
            outcome_symbol = "✅" if outcome == "passed" else "❌" if outcome == "failed" else "⏸️"

            # Add test details as a row in the table
            markdown_report += f"| {test_name} | {outcome_symbol} | {duration:.2f} sec | {message} |\n"

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
