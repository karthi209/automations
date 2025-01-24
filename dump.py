import subprocess
import os

def test_npm_cafile_configuration():
    """Test if npm's cafile configuration is set correctly and points to a valid file."""
    expected_cafile = "/etc/pki/tls/certs/ca-bundle.crt"

    # Step 1: Retrieve the current value of 'cafile' configuration
    result = subprocess.run(
        ["npm", "config", "get", "cafile"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
    actual_cafile = result.stdout.strip()

    # Step 2: Assert that the 'cafile' configuration matches the expected value
    assert actual_cafile == expected_cafile, (
        f"npm cafile configuration is {actual_cafile}, "
        f"but expected {expected_cafile}"
    )

    # Step 3: Check if the cafile path exists
    assert os.path.exists(actual_cafile), f"The cafile path {actual_cafile} does not exist."
