import subprocess
import os
import sys
import pytest

# Test 1: Check Python version
def test_python_version():
    """Ensure the installed Python version is correct."""
    expected_version = "3.8"  # Modify this based on your requirements
    try:
        result = subprocess.run(
            [sys.executable, "--version"], capture_output=True, text=True, check=True
        )
        version = result.stdout.strip()
        assert version.startswith(f"Python {expected_version}"), f"Expected version {expected_version}, but got {version}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run Python: {e}")

# Test 2: Check Python installation path
def test_python_installation_path():
    """Ensure Python is installed in the expected directory."""
    expected_path = "/usr/local/bin/python3"  # Modify this based on your expected Python installation path
    python_path = sys.executable
    assert python_path == expected_path, f"Expected Python path {expected_path}, but got {python_path}"

# Test 3: Check if Python is symlinked correctly
def test_python_symlink():
    """Ensure that the python3 executable is symlinked to the correct executable."""
    symlink_path = "/usr/bin/python3"  # Modify this path based on your system
    real_path = os.readlink(symlink_path)
    expected_path = sys.executable
    assert real_path == expected_path, f"Symlink {symlink_path} points to {real_path}, expected {expected_path}"

# Test 4: Check if python executable can run a simple script
def test_python_functionality():
    """Run a simple Python script to test functionality."""
    try:
        # Run a basic Python script to ensure Python can execute code
        result = subprocess.run(
            [sys.executable, "-c", "print('Hello World!')"],
            capture_output=True,
            text=True,
            check=True,
        )
        assert result.stdout.strip() == "Hello World!", f"Expected 'Hello World!', but got {result.stdout.strip()}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run Python script: {e}")

# Test 5: Check Python environment variables
def test_python_environment():
    """Ensure that Python's environment variables are set correctly."""
    python_env = os.environ.get("PYTHONPATH")
    assert python_env is not None, "PYTHONPATH is not set"
    assert os.path.exists(python_env), f"PYTHONPATH {python_env} does not exist"
    assert "site-packages" in python_env, "PYTHONPATH does not include site-packages"

# Test 6: Check Python package import (as a functionality test)
def test_python_package_import():
    """Ensure that a common Python package (e.g., os) can be imported."""
    try:
        import os  # Check if os package can be imported
        assert os.name == "posix" or os.name == "nt", f"Unexpected os.name: {os.name}"
    except ImportError as e:
        pytest.fail(f"Failed to import os module: {e}")

# Test 7: Check Python for correct system architecture
def test_python_architecture():
    """Ensure Python is the correct architecture (e.g., 64-bit)."""
    expected_architecture = "64bit"  # Modify as per your expected architecture
    architecture = sys.maxsize > 2**32 and "64bit" or "32bit"
    assert architecture == expected_architecture, f"Expected {expected_architecture}, but got {architecture}"

# Test 8: Check Python's site-packages directory
def test_python_site_packages():
    """Ensure that Python's site-packages directory exists and is accessible."""
    site_packages_dir = os.path.join(sys.prefix, "lib", "python" + sys.version[:3], "site-packages")
    assert os.path.exists(site_packages_dir), f"site-packages directory {site_packages_dir} does not exist"
    assert os.path.isdir(site_packages_dir), f"{site_packages_dir} is not a directory"
    





import subprocess
import os
import sys
import pytest

# Test 1: Check Git version
def test_git_version():
    """Ensure the installed Git version is correct."""
    expected_version = "2.34"  # Modify this based on your requirements
    try:
        result = subprocess.run(
            ["git", "--version"], capture_output=True, text=True, check=True
        )
        version = result.stdout.strip().split()[-1]
        assert version.startswith(f"{expected_version}"), f"Expected version {expected_version}, but got {version}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run Git: {e}")

# Test 2: Check Git installation path
def test_git_installation_path():
    """Ensure Git is installed in the expected directory."""
    expected_path = "/usr/local/bin/git"  # Modify this based on your expected Git installation path
    git_path = subprocess.run(
        ["which", "git"], capture_output=True, text=True, check=True
    ).stdout.strip()
    assert git_path == expected_path, f"Expected Git path {expected_path}, but got {git_path}"

# Test 3: Check if Git is symlinked correctly
def test_git_symlink():
    """Ensure that the git executable is symlinked to the correct executable."""
    symlink_path = "/usr/bin/git"  # Modify this path based on your system
    real_path = os.readlink(symlink_path)
    expected_path = subprocess.run(
        ["which", "git"], capture_output=True, text=True, check=True
    ).stdout.strip()
    assert real_path == expected_path, f"Symlink {symlink_path} points to {real_path}, expected {expected_path}"

# Test 4: Check if Git can run a simple command
def test_git_functionality():
    """Run a simple Git command to test functionality."""
    try:
        result = subprocess.run(
            ["git", "status"], capture_output=True, text=True, check=True
        )
        assert "fatal" not in result.stderr, f"Git command failed with error: {result.stderr}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run Git command: {e}")
    
# Test 5: Check Git environment variables
def test_git_environment():
    """Ensure Git's environment variables are set correctly."""
    git_env = subprocess.run(
        ["git", "config", "--list"], capture_output=True, text=True
    ).stdout.strip()
    assert "user.name" in git_env, "Git user.name is not set"
    assert "user.email" in git_env, "Git user.email is not set"

