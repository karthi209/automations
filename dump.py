import subprocess
import pytest

def run_command(command):
    """Helper function to run shell commands and return output"""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1  # Return error message and non-zero exit code

def test_node_installed():
    stdout, stderr, exit_code = run_command("node -v")
    assert exit_code == 0, f"Node.js is not installed or not in PATH. Error: {stderr}"
    assert stdout.startswith("v"), f"Unexpected Node.js version output: {stdout}"

def test_npm_installed():
    stdout, stderr, exit_code = run_command("npm -v")
    assert exit_code == 0, f"npm is not installed or not in PATH. Error: {stderr}"
    assert stdout.replace(".", "").isdigit(), f"Unexpected npm version output: {stdout}"

def test_nvm_installed():
    stdout, stderr, exit_code = run_command("command -v nvm")
    assert exit_code == 0, "nvm is not installed or not in PATH."
    assert "nvm" in stdout, f"Unexpected nvm command output: {stdout}"
