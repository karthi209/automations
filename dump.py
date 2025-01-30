---
- name: Verify Cosign Installation and Signing
  hosts: all
  gather_facts: false
  tasks:
    - name: Ensure test file exists
      ansible.builtin.copy:
        content: "test"
        dest: "/tmp/test.txt"
        mode: "0644"

    - name: Generate Cosign key pair (non-interactive)
      ansible.builtin.command:
        cmd: cosign generate-key-pair
      args:
        creates: /root/cosign.key  # Ensures it runs only if keys don't exist
      environment:
        COSIGN_PASSWORD: ""

    - name: Sign test file using Cosign
      ansible.builtin.command:
        cmd: cosign sign-blob --key /root/cosign.key /tmp/test.txt
      environment:
        COSIGN_PASSWORD: ""
      register: sign_output
      changed_when: "'Signature' in sign_output.stdout"

    - name: Verify signed file using Cosign
      ansible.builtin.command:
        cmd: cosign verify-blob --key /root/cosign.pub /tmp/test.txt.sig
      environment:
        COSIGN_PASSWORD: ""
      register: verify_output
      changed_when: false

    - name: Ensure Cosign verification is successful
      ansible.builtin.assert:
        that:
          - "'Verified OK' in verify_output.stdout"
        fail_msg: "Cosign verification failed!"
        success_msg: "Cosign verification succeeded!"






import os
import subprocess
import pytest

TEST_FILE = "/tmp/test.txt"
COSIGN_KEY = "/root/cosign.key"
COSIGN_PUB = "/root/cosign.pub"
SIGNATURE_FILE = "/tmp/test.txt.sig"

@pytest.fixture(scope="module", autouse=True)
def setup_test_file():
    """Create a test file before running tests."""
    with open(TEST_FILE, "w") as f:
        f.write("test")
    yield
    os.remove(TEST_FILE)
    if os.path.exists(SIGNATURE_FILE):
        os.remove(SIGNATURE_FILE)

@pytest.fixture(scope="module", autouse=True)
def setup_cosign_keys():
    """Generate Cosign keys if they don’t exist."""
    if not os.path.exists(COSIGN_KEY) or not os.path.exists(COSIGN_PUB):
        subprocess.run(["cosign", "generate-key-pair"], env={"COSIGN_PASSWORD": ""}, check=True)

@pytest.mark.order(1)
def test_cosign_installed():
    """Check if Cosign is installed."""
    result = subprocess.run(["cosign", "version"], capture_output=True, text=True)
    assert result.returncode == 0, "Cosign is not installed!"
    assert "Version:" in result.stdout, "Failed to fetch Cosign version."

@pytest.mark.order(2)
def test_cosign_sign():
    """Sign the test file using Cosign."""
    result = subprocess.run(
        ["cosign", "sign-blob", "--key", COSIGN_KEY, TEST_FILE],
        env={"COSIGN_PASSWORD": ""},
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Failed to sign file: {result.stderr}"
    assert os.path.exists(SIGNATURE_FILE), "Signature file was not created!"

@pytest.mark.order(3)
def test_cosign_verify():
    """Verify the signed test file using Cosign."""
    result = subprocess.run(
        ["cosign", "verify-blob", "--key", COSIGN_PUB, SIGNATURE_FILE],
        env={"COSIGN_PASSWORD": ""},
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Cosign verification failed: {result.stderr}"
    assert "Verified OK" in result.stdout, "Verification did not succeed!"
