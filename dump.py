import subprocess
import os
import re

def test_python3():
    tool_command = "python3"
    try:
        version_output = subprocess.check_output([tool_command, "--version"], stderr=subprocess.STDOUT).decode()
        version = version_output.strip()
        install_path = subprocess.check_output(["which", tool_command], stderr=subprocess.STDOUT).decode().strip()
        symlink = "No symlink"  # Add symlink logic if necessary
        
        return {
            "tool": "python3",
            "version": version,
            "install_path": install_path,
            "symlink": symlink
        }
    except subprocess.CalledProcessError:
        return {"tool": "python3", "version": "not installed", "install_path": "not found", "symlink": "not found"}
