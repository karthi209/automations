import subprocess
import sys
import pytest

def test_pip_installation():
    """Ensure databricks-sql-cli is installed via pip."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", "databricks-sql-cli"],
        capture_output=True,
        text=True
    )
    assert "Name: databricks-sql-cli" in result.stdout, "databricks-sql-cli is NOT installed."

def test_python_import():
    """Ensure databricks-sql-cli can be imported in Python."""
    try:
        import databricks_sql_cli  # This is the correct import
    except ImportError:
        pytest.fail("Python module 'databricks_sql_cli' not found.")

def test_cli_execution():
    """Ensure databricks-sql CLI runs without errors."""
    result = subprocess.run(
        ["databricks-sql", "--help"],
        capture_output=True,
        text=True
    )
    assert "Usage: databricks-sql [OPTIONS] COMMAND" in result.stdout, \
        f"databricks-sql CLI command failed.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

