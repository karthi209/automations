import subprocess
import json
import os

def get_version(tool_command):
    """Get the version of the tool by running '<tool_command> --version'."""
    try:
        version = subprocess.check_output([tool_command, "--version"], stderr=subprocess.STDOUT)
        return version.decode().strip()
    except subprocess.CalledProcessError:
        return f"{tool_command} version check failed"

def get_installation_path(tool_command):
    """Get the installation path of the tool by running 'which <tool_command>'."""
    try:
        path = subprocess.check_output(["which", tool_command], stderr=subprocess.STDOUT)
        return path.decode().strip()
    except subprocess.CalledProcessError:
        return f"{tool_command} installation path not found"

def get_symlink_target(tool_command):
    """Check if the tool is a symlink and return the target path."""
    if os.path.islink(tool_command):
        return os.readlink(tool_command)
    else:
        return "No symlink"

def test_tool(tool, expected_tool_info):
    """Test the tool by checking version, installation path, and symlink."""
    tool_command = expected_tool_info.get("command", tool)  # Default to tool name if no command is provided

    tool_info = {
        "tool": tool,
        "command": tool_command,
        "version": get_version(tool_command),
        "install_path": get_installation_path(tool_command),
        "symlink": get_symlink_target(tool_command),
    }

    # Log the results
    print(f"Results for {tool} (command: {tool_command}):")
    print(f"  Version: {tool_info['version']}")
    print(f"  Installation Path: {tool_info['install_path']}")
    print(f"  Symlink: {tool_info['symlink']}")

    # Check against expected values if provided
    if expected_tool_info:
        if "version" in expected_tool_info and expected_tool_info["version"] != tool_info["version"]:
            print(f"  Version mismatch for {tool}: Expected {expected_tool_info['version']}, got {tool_info['version']}")
        if "install_path" in expected_tool_info and expected_tool_info["install_path"] != tool_info["install_path"]:
            print(f"  Path mismatch for {tool}: Expected {expected_tool_info['install_path']}, got {tool_info['install_path']}")
        if "symlink" in expected_tool_info and expected_tool_info["symlink"] != tool_info["symlink"]:
            print(f"  Symlink mismatch for {tool}: Expected {expected_tool_info['symlink']}, got {tool_info['symlink']}")

    return tool_info

def main():
    # Load expected tool info from JSON
    try:
        with open('/tools_expected.json', 'r') as f:
            tools_expected = json.load(f)
    except FileNotFoundError:
        print("Expected tools file '/tools_expected.json' not found.")
        return

    # Test each tool listed in the JSON
    for tool, expected_info in tools_expected.items():
        test_tool(tool, expected_info)

if __name__ == "__main__":
    main()
