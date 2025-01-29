import pytest
import subprocess

@pytest.mark.parametrize("command", [
    ("ssh-keygen", "-F github.com")
])
def test_known_host(command):
    cmd, subcommand = command
    try:
        # Run the ssh-keygen command to check if github.com is in known_hosts
        result = subprocess.run([cmd, subcommand], capture_output=True, text=True, check=True)
        
        # Check if github.com is found in the known_hosts file
        if "github.com" in result.stdout:
            assert True, "github.com is a known host"
        else:
            assert False, "github.com is not a known host"
    except FileNotFoundError:
        pytest.fail(f"{cmd} is not installed")
    except subprocess.CalledProcessError:
        pytest.fail(f"{cmd} command failed")
