import subprocess
import json

# Path to the tool version config file
TOOL_VERSION_CONFIG = 'tool_version_config.json'

# Function to extract the version of a tool using the command from the config
def get_version(tool, command):
    try:
        # Execute the command and capture the output
        result = subprocess.check_output(command, shell=True, text=True)
        
        # If we get a result, strip and return the version
        if result:
            return f"{tool}: {result.strip()}"
        else:
            return f"{tool}: Version not found"
    except subprocess.CalledProcessError:
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
