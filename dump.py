import subprocess
import pytest

def get_python_version():
    result = subprocess.run(["python3", "--version"], capture_output=True, text=True)
    return result.stdout.strip()

def test_python_version():
    assert "Python 3" in get_python_version()

def test_python_installation_path():
    result = subprocess.run(["which", "python3"], capture_output=True, text=True)
    assert "/usr/bin/python3" in result.stdout.strip()

def test_python_symlink():
    result = subprocess.run(["ls", "-l", "/usr/bin/python3"], capture_output=True, text=True)
    assert "/usr/bin/python3" in result.stdout.strip()



import subprocess
import pytest

def get_git_version():
    result = subprocess.run(["git", "--version"], capture_output=True, text=True)
    return result.stdout.strip()

def test_git_version():
    assert "git version" in get_git_version()

def test_git_installation_path():
    result = subprocess.run(["which", "git"], capture_output=True, text=True)
    assert "/usr/bin/git" in result.stdout.strip()

def test_git_symlink():
    result = subprocess.run(["ls", "-l", "/usr/bin/git"], capture_output=True, text=True)
    assert "/usr/bin/git" in result.stdout.strip()




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
