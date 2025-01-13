import subprocess

def test_python3_version():
    """Check the Python version"""
    version = subprocess.check_output(["python3", "--version"]).decode("utf-8").strip()
    print(f"Python version: {version}")
    assert version.startswith("Python 3")

def test_python3_installation_path():
    """Check Python installation path"""
    install_path = subprocess.check_output(["which", "python3"]).decode("utf-8").strip()
    print(f"Python installation path: {install_path}")
    assert "/usr/bin/python3" in install_path, f"Expected python3 in /usr/bin but found {install_path}"

def test_python3_symlink():
    """Check if python3 is a symlink"""
    symlink = subprocess.check_output(["ls", "-l", "/usr/bin/python3"]).decode("utf-8").strip()
    print(f"Python symlink info: {symlink}")
    assert "python3" in symlink, "Python symlink not found or pointing incorrectly"

def test_python3_basic_functionality():
    """Ensure Python can run a simple script"""
    script = 'print("Hello, World!")'
    result = subprocess.check_output(["python3", "-c", script]).decode("utf-8").strip()
    print(f"Python script output: {result}")
    assert result == "Hello, World!", f"Unexpected output: {result}"

if __name__ == "__main__":
    test_python3_version()
    test_python3_installation_path()
    test_python3_symlink()
    test_python3_basic_functionality()




import subprocess

def test_maven_version():
    """Check Maven version"""
    version = subprocess.check_output(["mvn", "--version"]).decode("utf-8").strip()
    print(f"Maven version: {version}")
    assert "Apache Maven" in version, f"Expected 'Apache Maven' in version info, but found {version}"

def test_maven_installation_path():
    """Check Maven installation path"""
    install_path = subprocess.check_output(["which", "mvn"]).decode("utf-8").strip()
    print(f"Maven installation path: {install_path}")
    assert "/usr/bin/mvn" in install_path, f"Expected mvn in /usr/bin but found {install_path}"

def test_maven_symlink():
    """Check if Maven is a symlink"""
    symlink = subprocess.check_output(["ls", "-l", "/usr/bin/mvn"]).decode("utf-8").strip()
    print(f"Maven symlink info: {symlink}")
    assert "mvn" in symlink, "Maven symlink not found or pointing incorrectly"

def test_maven_basic_functionality():
    """Run a basic maven command to verify functionality"""
    result = subprocess.check_output(["mvn", "--version"]).decode("utf-8").strip()
    print(f"Basic Maven functionality check: {result}")
    assert "Apache Maven" in result, f"Unexpected Maven version: {result}"

if __name__ == "__main__":
    test_maven_version()
    test_maven_installation_path()
    test_maven_symlink()
    test_maven_basic_functionality()




import subprocess

def test_curl_version():
    """Check cURL version"""
    version = subprocess.check_output(["curl", "--version"]).decode("utf-8").strip()
    print(f"cURL version: {version}")
    assert "curl" in version, f"Expected 'curl' in version info, but found {version}"

def test_curl_installation_path():
    """Check cURL installation path"""
    install_path = subprocess.check_output(["which", "curl"]).decode("utf-8").strip()
    print(f"cURL installation path: {install_path}")
    assert "/usr/bin/curl" in install_path, f"Expected curl in /usr/bin but found {install_path}"

def test_curl_symlink():
    """Check if cURL is a symlink"""
    symlink = subprocess.check_output(["ls", "-l", "/usr/bin/curl"]).decode("utf-8").strip()
    print(f"cURL symlink info: {symlink}")
    assert "curl" in symlink, "cURL symlink not found or pointing incorrectly"

def test_curl_basic_functionality():
    """Check if cURL can fetch a URL"""
    url = "https://www.google.com"
    result = subprocess.check_output(["curl", "-I", url]).decode("utf-8").strip()
    print(f"cURL fetch response: {result}")
    assert "HTTP" in result, f"Expected 'HTTP' in cURL response, but got {result}"

if __name__ == "__main__":
    test_curl_version()
    test_curl_installation_path()
    test_curl_symlink()
    test_curl_basic_functionality()




import subprocess

def test_git_version():
    """Check Git version"""
    version = subprocess.check_output(["git", "--version"]).decode("utf-8").strip()
    print(f"Git version: {version}")
    assert "git" in version, f"Expected 'git' in version info, but found {version}"

def test_git_installation_path():
    """Check Git installation path"""
    install_path = subprocess.check_output(["which", "git"]).decode("utf-8").strip()
    print(f"Git installation path: {install_path}")
    assert "/usr/bin/git" in install_path, f"Expected git in /usr/bin but found {install_path}"

def test_git_symlink():
    """Check if Git is a symlink"""
    symlink = subprocess.check_output(["ls", "-l", "/usr/bin/git"]).decode("utf-8").strip()
    print(f"Git symlink info: {symlink}")
    assert "git" in symlink, "Git symlink not found or pointing incorrectly"

def test_git_basic_functionality():
    """Run a basic git command to verify functionality"""
    result = subprocess.check_output(["git", "--version"]).decode("utf-8").strip()
    print(f"Basic Git functionality check: {result}")
    assert "git" in result, f"Unexpected Git version: {result}"

if __name__ == "__main__":
    test_git_version()
    test_git_installation_path()
    test_git_symlink()
    test_git_basic_functionality()
