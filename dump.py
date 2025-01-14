import subprocess
import pytest

def get_maven_version():
    result = subprocess.run(["mvn", "--version"], capture_output=True, text=True)
    return result.stdout.strip()

def test_maven_version():
    assert "Apache Maven" in get_maven_version()

def test_maven_installation_path():
    result = subprocess.run(["which", "mvn"], capture_output=True, text=True)
    assert "/usr/bin/mvn" in result.stdout.strip()

def test_maven_symlink():
    result = subprocess.run(["ls", "-l", "/usr/bin/mvn"], capture_output=True, text=True)
    assert "/usr/bin/mvn" in result.stdout.strip()
