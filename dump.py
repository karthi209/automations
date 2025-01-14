import subprocess
import os
import sys
import pytest

# Test 1: Check Maven version
def test_maven_version():
    """Ensure the installed Maven version is correct."""
    expected_version = "3.8"  # Modify this based on your requirements
    try:
        result = subprocess.run(
            ["mvn", "-v"], capture_output=True, text=True, check=True
        )
        version = result.stdout.strip().splitlines()[0]
        assert version.startswith(f"Apache Maven {expected_version}"), f"Expected version {expected_version}, but got {version}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run Maven: {e}")

# Test 2: Check Maven installation path
def test_maven_installation_path():
    """Ensure Maven is installed in the expected directory."""
    expected_path = "/usr/local/bin/mvn"  # Modify this based on your expected Maven installation path
    maven_path = subprocess.run(
        ["which", "mvn"], capture_output=True, text=True, check=True
    ).stdout.strip()
    assert maven_path == expected_path, f"Expected Maven path {expected_path}, but got {maven_path}"

# Test 3: Check if Maven is symlinked correctly
def test_maven_symlink():
    """Ensure that the mvn executable is symlinked to the correct executable."""
    symlink_path = "/usr/bin/mvn"  # Modify this path based on your system
    real_path = os.readlink(symlink_path)
    expected_path = subprocess.run(
        ["which", "mvn"], capture_output=True, text=True, check=True
    ).stdout.strip()
    assert real_path == expected_path, f"Symlink {symlink_path} points to {real_path}, expected {expected_path}"

# Test 4: Check if Maven can run a simple command
def test_maven_functionality():
    """Run a simple Maven command to test functionality."""
    try:
        result = subprocess.run(
            ["mvn", "clean", "validate"], capture_output=True, text=True, check=True
        )
        assert "BUILD SUCCESS" in result.stdout, f"Maven command failed with output: {result.stdout}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run Maven command: {e}")

# Test 5: Check Maven environment variables
def test_maven_environment():
    """Ensure Maven's environment variables are set correctly."""
    maven_env = subprocess.run(
        ["mvn", "--version"], capture_output=True, text=True
    ).stdout.strip()
    assert "MAVEN_HOME" in maven_env, "MAVEN_HOME is not set"
    assert "JAVA_HOME" in maven_env, "JAVA_HOME is not set"
