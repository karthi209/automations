import subprocess
import json

# Path to the tool version config file
TOOL_VERSION_CONFIG = 'tool_version_config.json'
OUTPUT_FILE = '/tmp/test_tools/tool_versions.json'  # Output file location inside the container

# Function to extract the version of a tool using the command from the config
def get_version(tool, command):
    try:
        # Execute the command and capture the output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Check if the command ran successfully
        if result.returncode == 0:
            version = result.stdout.strip()
            if version:
                return f"{tool}: {version}"
            else:
                return f"{tool}: Version not found"
        else:
            return f"{tool}: Error executing command"
    except Exception as e:
        return f"{tool}: {str(e)}"

# Function to load the tool version config and fetch versions for each tool
def get_tool_versions():
    tool_versions = {}
    
    try:
        with open(TOOL_VERSION_CONFIG, 'r') as f:
            tools_config = json.load(f)

        # Loop through each tool in the config and fetch its version
        for tool, details in tools_config.items():
            command = details.get('command', '')
            if command:
                tool_versions[tool] = get_version(tool, command)
            else:
                tool_versions[tool] = f"{tool}: No command found in config"
    
    except FileNotFoundError:
        print(f"Error: {TOOL_VERSION_CONFIG} file not found")
    except json.JSONDecodeError:
        print(f"Error: Failed to parse {TOOL_VERSION_CONFIG}, invalid JSON")
    
    # Write the results to a file
    with open(OUTPUT_FILE, 'w') as outfile:
        json.dump(tool_versions, outfile, indent=4)
    
    print(f"Tool versions saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    get_tool_versions()
