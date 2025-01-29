import pytest
import subprocess

@pytest.mark.parametrize("command", [
    ("git", "--version"),
    ("git-lfs", "--version"),
    ("gh", "--version"),
])
def test_command_installed(command):
    cmd, version_flag = command
    try:
        result = subprocess.run([cmd, version_flag], capture_output=True, text=True, check=True)
        assert result.returncode == 0, f"{cmd} is not installed or not working correctly"
        assert result.stdout, f"{cmd} version output is empty"
    except FileNotFoundError:
        pytest.fail(f"{cmd} is not installed")
    except subprocess.CalledProcessError:
        pytest.fail(f"{cmd} command failed")
