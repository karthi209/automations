import subprocess

def is_pip_package_installed(package_name):
    """Returns True if the pip package is installed, otherwise False."""
    try:
        result = subprocess.run(
            ["python3", "-m", "pip", "show", package_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return bool(result.stdout)  # If output exists, package is installed
    except subprocess.CalledProcessError:
        return False

def test_numpy_installed():
    """Test if numpy is installed."""
    assert is_pip_package_installed("numpy"), "numpy is not installed!"

def test_multiple_pip_packages():
    """Test multiple pip packages are installed."""
    packages = ["numpy", "pandas", "requests"]
    
    for package in packages:
        assert is_pip_package_installed(package), f"{package} is not installed!"




import subprocess
import json

def is_az_extension_installed(extension_name):
    """Returns True if the Azure CLI extension is installed, otherwise False."""
    try:
        result = subprocess.run(
            ["az", "extension", "show", "--name", extension_name, "--output", "json"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        json.loads(result.stdout)  # If JSON loads correctly, extension exists
        return True
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return False

def test_azure_devops_extension_installed():
    """Test if the azure-devops extension is installed."""
    assert is_az_extension_installed("azure-devops"), "azure-devops extension is not installed!"

def test_multiple_az_extensions():
    """Test multiple Azure CLI extensions are installed."""
    extensions = ["azure-devops", "account"]
    
    for extension in extensions:
        assert is_az_extension_installed(extension), f"{extension} extension is not installed!"
