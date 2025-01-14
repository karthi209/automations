import subprocess
import pytest
import os

def get_docker_version():
    result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
    return result.stdout.strip()

def test_docker_version():
    assert "Docker" in get_docker_version()

def test_docker_installation_path():
    result = subprocess.run(["which", "docker"], capture_output=True, text=True)
    assert "/usr/bin/docker" in result.stdout.strip()

def test_docker_symlink():
    result = subprocess.run(["ls", "-l", "/usr/bin/docker"], capture_output=True, text=True)
    assert "/usr/bin/docker" in result.stdout.strip()

def test_docker_executable():
    result = subprocess.run(["docker", "--help"], capture_output=True, text=True)
    assert result.returncode == 0

def test_docker_home_env_var():
    result = subprocess.run(["echo", "$DOCKER_HOME"], capture_output=True, text=True, shell=True)
    assert result.stdout.strip() != ""  # Ensure DOCKER_HOME is set




import subprocess
import pytest
import os

def get_kubectl_version():
    result = subprocess.run(["kubectl", "version", "--client"], capture_output=True, text=True)
    return result.stdout.strip()

def test_kubectl_version():
    assert "Client Version" in get_kubectl_version()

def test_kubectl_installation_path():
    result = subprocess.run(["which", "kubectl"], capture_output=True, text=True)
    assert "/usr/bin/kubectl" in result.stdout.strip()

def test_kubectl_symlink():
    result = subprocess.run(["ls", "-l", "/usr/bin/kubectl"], capture_output=True, text=True)
    assert "/usr/bin/kubectl" in result.stdout.strip()

def test_kubectl_executable():
    result = subprocess.run(["kubectl", "--help"], capture_output=True, text=True)
    assert result.returncode == 0

def test_kubectl_home_env_var():
    result = subprocess.run(["echo", "$KUBECTL_HOME"], capture_output=True, text=True, shell=True)
    assert result.stdout.strip() != ""  # Ensure KUBECTL_HOME is set





import subprocess
import pytest
import os

def get_terraform_version():
    result = subprocess.run(["terraform", "--version"], capture_output=True, text=True)
    return result.stdout.strip()

def test_terraform_version():
    assert "Terraform" in get_terraform_version()

def test_terraform_installation_path():
    result = subprocess.run(["which", "terraform"], capture_output=True, text=True)
    assert "/usr/bin/terraform" in result.stdout.strip()

def test_terraform_symlink():
    result = subprocess.run(["ls", "-l", "/usr/bin/terraform"], capture_output=True, text=True)
    assert "/usr/bin/terraform" in result.stdout.strip()

def test_terraform_executable():
    result = subprocess.run(["terraform", "--help"], capture_output=True, text=True)
    assert result.returncode == 0

def test_terraform_home_env_var():
    result = subprocess.run(["echo", "$TERRAFORM_HOME"], capture_output=True, text=True, shell=True)
    assert result.stdout.strip() != ""  # Ensure TERRAFORM_HOME is set




import subprocess
import pytest
import os

def get_node_version():
    result = subprocess.run(["node", "--version"], capture_output=True, text=True)
    return result.stdout.strip()

def test_node_version():
    assert "v" in get_node_version()  # Node.js version should start with 'v'

def test_node_installation_path():
    result = subprocess.run(["which", "node"], capture_output=True, text=True)
    assert "/usr/bin/node" in result.stdout.strip()

def test_node_symlink():
    result = subprocess.run(["ls", "-l", "/usr/bin/node"], capture_output=True, text=True)
    assert "/usr/bin/node" in result.stdout.strip()

def test_node_executable():
    result = subprocess.run(["node", "--help"], capture_output=True, text=True)
    assert result.returncode == 0

def test_node_home_env_var():
    result = subprocess.run(["echo", "$NODE_HOME"], capture_output=True, text=True, shell=True)
    assert result.stdout.strip() != ""  # Ensure NODE_HOME is set



import subprocess
import pytest
import os

def get_python_version():
    result = subprocess.run(["python", "--version"], capture_output=True, text=True)
    return result.stdout.strip()

def test_python_version():
    assert "Python" in get_python_version()

def test_python_installation_path():
    result = subprocess.run(["which", "python"], capture_output=True, text=True)
    assert "/usr/bin/python" in result.stdout.strip()

def test_python_symlink():
    result = subprocess.run(["ls", "-l", "/usr/bin/python"], capture_output=True, text=True)
    assert "/usr/bin/python" in result.stdout.strip()

def test_python_executable():
    result = subprocess.run(["python", "--help"], capture_output=True, text=True)
    assert result.returncode == 0

def test_python_home_env_var():
    result = subprocess.run(["echo", "$PYTHON_HOME"], capture_output=True, text=True, shell=True)
    assert result.stdout.strip() != ""  # Ensure PYTHON_HOME is set




import subprocess
import pytest
import os

def get_mysql_version():
    result = subprocess.run(["mysql", "--version"], capture_output=True, text=True)
    return result.stdout.strip()

def test_mysql_version():
    assert "mysql" in get_mysql_version()

def test_mysql_installation_path():
    result = subprocess.run(["which", "mysql"], capture_output=True, text=True)
    assert "/usr/bin/mysql" in result.stdout.strip()

def test_mysql_symlink():
    result = subprocess.run(["ls", "-l", "/usr/bin/mysql"], capture_output=True, text=True)
    assert "/usr/bin/mysql" in result.stdout.strip()

def test_mysql_executable():
    result = subprocess.run(["mysql", "--help"], capture_output=True, text=True)
    assert result.returncode == 0

def test_mysql_home_env_var():
    result = subprocess.run(["echo", "$MYSQL_HOME"], capture_output=True, text=True, shell=True)
    assert result.stdout.strip() != ""  # Ensure MYSQL_HOME is set



import subprocess
import pytest
import os

def get_ruby_version():
    result = subprocess.run(["ruby", "--version"], capture_output=True, text=True)
    return result.stdout.strip()

def test_ruby_version():
    assert "ruby" in get_ruby_version()

def test_ruby_installation_path():
    result = subprocess.run(["which", "ruby"], capture_output=True, text=True)
    assert "/usr/bin/ruby" in result.stdout.strip()

def test_ruby_symlink():
    result = subprocess.run(["ls", "-l", "/usr/bin/ruby"], capture_output=True, text=True)
    assert "/usr/bin/ruby" in result.stdout.strip()

def test_ruby_executable():
    result = subprocess.run(["ruby", "--help"], capture_output=True, text=True)
    assert result.returncode == 0

def test_ruby_home_env_var():
    result = subprocess.run(["echo", "$RUBY_HOME"], capture_output=True, text=True, shell=True)
    assert result.stdout.strip() != ""  # Ensure RUBY_HOME is set




import subprocess
import pytest
import os

def get_go_version():
    result = subprocess.run(["go", "version"], capture_output=True, text=True)
    return result.stdout.strip()

def test_go_version():
    assert "go" in get_go_version()

def test_go_installation_path():
    result = subprocess.run(["which", "go"], capture_output=True, text=True)
    assert "/usr/bin/go" in result.stdout.strip()

def test_go_symlink():
    result = subprocess.run(["ls", "-l", "/usr/bin/go"], capture_output=True, text=True)
    assert "/usr/bin/go" in result.stdout.strip()

def test_go_executable():
    result = subprocess.run(["go", "help"], capture_output=True, text=True)
    assert result.returncode == 0

def test_go_home_env_var():
    result = subprocess.run(["echo", "$GO_HOME"], capture_output=True, text=True, shell=True)
    assert result.stdout.strip() != ""  # Ensure GO_HOME is set
