import subprocess
import json

# Path to the tool version config file
TOOL_VERSION_CONFIG = 'tool_version_config.json'

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
    try:
        with open(TOOL_VERSION_CONFIG, 'r') as f:
            tools_config = json.load(f)

        # Loop through each tool in the config and fetch its version
        for tool, details in tools_config.items():
            command = details.get('command', '')
            if command:
                print(get_version(tool, command))
            else:
                print(f"{tool}: No command found in config")
    
    except FileNotFoundError:
        print(f"Error: {TOOL_VERSION_CONFIG} file not found")
    except json.JSONDecodeError:
        print(f"Error: Failed to parse {TOOL_VERSION_CONFIG}, invalid JSON")
    
if __name__ == '__main__':
    get_tool_versions()
