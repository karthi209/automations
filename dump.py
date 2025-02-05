import json
import subprocess
import shutil
from pathlib import Path

TOOL_VERSION_CONFIG = '/tmp/test_tools/tool_version_config.json'
OUTPUT_FILE = '/tmp/test_tools/tool_versions.json'

def get_version(tool, command):
    """Check the version of a tool by running its version command."""
    if not shutil.which(tool.split()[0]):  # Handle cases like "python3" vs "python"
        return "Not installed"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip() or result.stderr.strip()  # Some tools output version to stderr
        return f"Error executing: {command}"
    except Exception as e:
        return str(e)

def get_tool_versions():
    """Read the tool config and fetch version information for each tool."""
    tool_versions = {}
    try:
        with open(TOOL_VERSION_CONFIG, 'r') as f:
            tools_config = json.load(f)
        
        # Add version info for each configured tool
        for tool, details in tools_config.items():
            command = details.get('command', '')
            tool_versions[tool] = get_version(tool, command) if command else "No command found"
        
    except Exception as e:
        print(f"Error: {str(e)}")
        tool_versions["error"] = str(e)
    
    # Write results
    with open(OUTPUT_FILE, 'w') as outfile:
        json.dump(tool_versions, outfile, indent=2, sort_keys=True)

if __name__ == "__main__":
    get_tool_versions()
