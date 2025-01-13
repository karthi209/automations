import subprocess

# List of tools and their command to check the version
tools = [
    ("python3", "python3 --version"),
    ("maven", "mvn --version"),
    ("node", "node --version"),
    ("npm", "npm --version"),
    ("git", "git --version"),
    ("docker", "docker --version"),
    ("java", "java -version")
]

# Function to check the tool installation and version
def check_tool_installation(tool_name, command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{tool_name} is installed: {result.stdout.decode().strip()}")
    except subprocess.CalledProcessError as e:
        print(f"{tool_name} failed to install: {e.stderr.decode().strip()}")
        raise Exception(f"{tool_name} installation check failed.")

# Run checks for all tools
for tool, command in tools:
    check_tool_installation(tool, command)
