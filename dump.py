import subprocess
import pytest
import os

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

def test_maven_executable():
    result = subprocess.run(["mvn", "--help"], capture_output=True, text=True)
    assert result.returncode == 0  # If mvn executes successfully, return code should be 0

def test_maven_home_env_var():
    result = subprocess.run(["echo", "$MAVEN_HOME"], capture_output=True, text=True, shell=True)
    assert result.stdout.strip() != ""  # Ensure MAVEN_HOME is set

def test_maven_clean():
    result = subprocess.run(["mvn", "clean"], capture_output=True, text=True)
    assert result.returncode == 0  # mvn clean should run without errors

def test_maven_settings_xml_exists():
    maven_settings_path = os.path.expanduser("~/.m2/settings.xml")
    assert os.path.exists(maven_settings_path)  # Ensure settings.xml exists in the default Maven location

def test_maven_local_repository_exists():
    local_repo_path = os.path.expanduser("~/.m2/repository")
    assert os.path.exists(local_repo_path)  # Ensure the local repository exists
