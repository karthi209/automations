safe_subprocess_call(["docker", "exec", container_name, "python3", "-c", """
import json, subprocess

TOOL_VERSION_CONFIG = '/tmp/test_tools/tool_version_config.json'
OUTPUT_FILE = '/tmp/test_tools/tool_versions.json'

def get_version(tool, command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else "0.0.0"
    except Exception as e:
        return str(e)

def get_tool_versions():
    tool_versions = {}
    try:
        with open(TOOL_VERSION_CONFIG, 'r') as f:
            tools_config = json.load(f)
        for tool, details in tools_config.items():
            command = details.get('command', '')
            tool_versions[tool] = get_version(tool, command) if command else "No command found"
    except Exception as e:
        print(f"Error: {str(e)}")
    with open(OUTPUT_FILE, 'w') as outfile:
        json.dump(tool_versions, outfile, indent=4)

get_tool_versions()
"""], "execute tool version retrieval inside container")
