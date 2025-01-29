import pytest
import subprocess

@pytest.mark.parametrize("command", [
    ("ssh-keygen", "-F github.com")
])
def test_known_host(command):
    cmd, subcommand = command
    try:
        # Run the ssh-keygen command to check if github.com is in known_hosts
        result = subprocess.run([cmd, subcommand], capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode != 0:
            if "no hostkey found" in result.stderr:
                # Known hosts file is not present or github.com is not found
                pytest.fail("GitHub is not a known host (or known_hosts file is missing).")
            else:
                # Some other failure (command not found, etc.)
                pytest.fail(f"ssh-keygen command failed: {result.stderr}")

        # Check if github.com is found in the known_hosts file
        if "github.com" in result.stdout:
            assert True, "github.com is a known host"
        else:
            pytest.fail("github.com is not listed as a known host.")
    
    except FileNotFoundError:
        pytest.fail(f"{cmd} is not installed. Please install SSH utilities.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"{cmd} command failed with error: {e}")
