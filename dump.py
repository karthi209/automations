import subprocess
import os
import pytest

COSIGN_PASSWORD = ""

@pytest.fixture(scope="module")
def setup_files():
    """Setup test file and generate Cosign keys."""
    # Create a test file
    with open("/tmp/test.txt", "w") as f:
        f.write("test")

    # Generate Cosign key pair if not exists
    if not os.path.exists("/root/cosign.key") or not os.path.exists("/root/cosign.pub"):
        subprocess.run(["cosign", "generate-key-pair"], env={"COSIGN_PASSWORD": COSIGN_PASSWORD}, check=True)

    yield

    # Cleanup
    os.remove("/tmp/test.txt")
    os.remove("/tmp/test.txt.sig")

def test_cosign_sign_and_verify(setup_files):
    """Test signing and verifying a file using Cosign."""

    # Sign file
    sign_cmd = ["cosign", "sign-blob", "-y", "--key", "/root/cosign.key", "/tmp/test.txt"]
    sign_proc = subprocess.run(sign_cmd, env={"COSIGN_PASSWORD": COSIGN_PASSWORD}, check=True, capture_output=True, text=True)
    signature = sign_proc.stdout.strip()

    # Save signature to a file
    with open("/tmp/test.txt.sig", "w") as sig_file:
        sig_file.write(signature)

    # Verify signature
    verify_cmd = ["cosign", "verify-blob", "--key", "/root/cosign.pub", "--signature", "/tmp/test.txt.sig", "/tmp/test.txt"]
    verify_proc = subprocess.run(verify_cmd, env={"COSIGN_PASSWORD": COSIGN_PASSWORD}, capture_output=True, text=True)

    assert "Verified OK" in verify_proc.stdout, "Cosign verification failed!"
