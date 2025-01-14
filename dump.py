import subprocess
import pytest
import os

def get_github_cli_version():
    result = subprocess.run(["gh", "--version"], capture_output=True, text=True)
    return result.stdout.strip()

def test_github_cli_version():
    assert "gh" in get_github_cli_version()

def test_github_cli_installation_path():
    result = subprocess.run(["which", "gh"], capture_output=True, text=True)
    assert "/usr/bin/gh" in result.stdout.strip()

def test_github_cli_symlink():
    result = subprocess.run(["ls", "-l", "/usr/bin/gh"], capture_output=True, text=True)
    assert "/usr/bin/gh" in result.stdout.strip()

def test_github_cli_executable():
    result = subprocess.run(["gh", "--help"], capture_output=True, text=True)
    assert result.returncode == 0

def test_github_cli_home_env_var():
    result = subprocess.run(["echo", "$GH_HOME"], capture_output=True, text=True, shell=True)
    assert result.stdout.strip() != ""  # Ensure GH_HOME is set





import subprocess
import pytest
import os

def get_az_cli_version():
    result = subprocess.run(["az", "--version"], capture_output=True, text=True)
    return result.stdout.strip()

def test_az_cli_version():
    assert "azure-cli" in get_az_cli_version()

def test_az_cli_installation_path():
    result = subprocess.run(["which", "az"], capture_output=True, text=True)
    assert "/usr/bin/az" in result.stdout.strip()

def test_az_cli_symlink():
    result = subprocess.run(["ls", "-l", "/usr/bin/az"], capture_output=True, text=True)
    assert "/usr/bin/az" in result.stdout.strip()

def test_az_cli_executable():
    result = subprocess.run(["az", "--help"], capture_output=True, text=True)
    assert result.returncode == 0

def test_az_cli_home_env_var():
    result = subprocess.run(["echo", "$AZ_HOME"], capture_output=True, text=True, shell=True)
    assert result.stdout.strip() != ""  # Ensure AZ_HOME is set





import subprocess
import pytest
import os

def get_bluemix_cli_version():
    result = subprocess.run(["bluemix", "--version"], capture_output=True, text=True)
    return result.stdout.strip()

def test_bluemix_cli_version():
    assert "Bluemix" in get_bluemix_cli_version()

def test_bluemix_cli_installation_path():
    result = subprocess.run(["which", "bluemix"], capture_output=True, text=True)
    assert "/usr/bin/bluemix" in result.stdout.strip()

def test_bluemix_cli_symlink():
    result = subprocess.run(["ls", "-l", "/usr/bin/bluemix"], capture_output=True, text=True)
    assert "/usr/bin/bluemix" in result.stdout.strip()

def test_bluemix_cli_executable():
    result = subprocess.run(["bluemix", "--help"], capture_output=True, text=True)
    assert result.returncode == 0

def test_bluemix_cli_home_env_var():
    result = subprocess.run(["echo", "$BLUEMIX_HOME"], capture_output=True, text=True, shell=True)
    assert result.stdout.strip() != ""  # Ensure BLUEMIX_HOME is set



import subprocess
import pytest
import os

def get_ibmcloud_cli_version():
    result = subprocess.run(["ibmcloud", "--version"], capture_output=True, text=True)
    return result.stdout.strip()

def test_ibmcloud_cli_version():
    assert "IBM Cloud" in get_ibmcloud_cli_version()

def test_ibmcloud_cli_installation_path():
    result = subprocess.run(["which", "ibmcloud"], capture_output=True, text=True)
    assert "/usr/bin/ibmcloud" in result.stdout.strip()

def test_ibmcloud_cli_symlink():
    result = subprocess.run(["ls", "-l", "/usr/bin/ibmcloud"], capture_output=True, text=True)
    assert "/usr/bin/ibmcloud" in result.stdout.strip()

def test_ibmcloud_cli_executable():
    result = subprocess.run(["ibmcloud", "--help"], capture_output=True, text=True)
    assert result.returncode == 0

def test_ibmcloud_cli_home_env_var():
    result = subprocess.run(["echo", "$IBMCLOUD_HOME"], capture_output=True, text=True, shell=True)
    assert result.stdout.strip() != ""  # Ensure IBMCLOUD_HOME is set




import subprocess
import pytest
import os

def get_sqlcmd_version():
    result = subprocess.run(["sqlcmd", "--version"], capture_output=True, text=True)
    return result.stdout.strip()

def test_sqlcmd_version():
    assert "sqlcmd" in get_sqlcmd_version()

def test_sqlcmd_installation_path():
    result = subprocess.run(["which", "sqlcmd"], capture_output=True, text=True)
    assert "/usr/bin/sqlcmd" in result.stdout.strip()

def test_sqlcmd_symlink():
    result = subprocess.run(["ls", "-l", "/usr/bin/sqlcmd"], capture_output=True, text=True)
    assert "/usr/bin/sqlcmd" in result.stdout.strip()

def test_sqlcmd_executable():
    result = subprocess.run(["sqlcmd", "--help"], capture_output=True, text=True)
    assert result.returncode == 0

def test_sqlcmd_home_env_var():
    result = subprocess.run(["echo", "$SQLCMD_HOME"], capture_output=True, text=True, shell=True)
    assert result.stdout.strip() != ""  # Ensure SQLCMD_HOME is set




import subprocess
import pytest
import os

def get_psql_version():
    result = subprocess.run(["psql", "--version"], capture_output=True, text=True)
    return result.stdout.strip()

def test_psql_version():
    assert "psql" in get_psql_version()

def test_psql_installation_path():
    result = subprocess.run(["which", "psql"], capture_output=True, text=True)
    assert "/usr/bin/psql" in result.stdout.strip()

def test_psql_symlink():
    result = subprocess.run(["ls", "-l", "/usr/bin/psql"], capture_output=True, text=True)
    assert "/usr/bin/psql" in result.stdout.strip()

def test_psql_executable():
    result = subprocess.run(["psql", "--help"], capture_output=True, text=True)
    assert result.returncode == 0

def test_psql_home_env_var():
    result = subprocess.run(["echo", "$PSQL_HOME"], capture_output=True, text=True, shell=True)
    assert result.stdout.strip() != ""  # Ensure PSQL_HOME is set
