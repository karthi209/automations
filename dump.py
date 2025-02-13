import sys
import json
import glob

def process_report(file):
    try:
        with open(file, 'r') as f:
            data = json.load(f)
            summary = f"## Report: {file}\n"
            summary += f"Total Tests: {data.get('total', 'N/A')}\n"
            summary += f"Passed: {data.get('passed', 'N/A')}, Failed: {data.get('failed', 'N/A')}\n"
            summary += "-" * 40 + "\n"
            return summary
    except Exception as e:
        return f"Error processing {file}: {e}\n"

if __name__ == "__main__":
    report_files = sys.argv[1:] if len(sys.argv) > 1 else glob.glob("test_report_*.json")

    if not report_files:
        print("No test report files found.")
        sys.exit(1)

    report_content = "# Integration Test Summary\n\n"
    for file in sorted(report_files):
        report_content += process_report(file)

    with open("test_results.md", "w") as f:
        f.write(report_content)

    print("Test summary generated successfully.")
