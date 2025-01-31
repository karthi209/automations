import subprocess
import sys

def check_pip_installation():
    """Check if databricks-sql-cli is installed via pip."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", "databricks-sql-cli"],
        capture_output=True,
        text=True
    )
    if "Name: databricks-sql-cli" not in result.stdout:
        print("[ERROR] databricks-sql-cli is NOT installed.")
        sys.exit(1)
    print("[OK] databricks-sql-cli is installed.")

def check_python_import():
    """Check if databricks-sql-cli can be imported in Python."""
    try:
        import databricks_sql_cli
        print("[OK] Python import for databricks_sql_cli is successful.")
    except ImportError:
        print("[ERROR] Python module 'databricks_sql_cli' not found.")
        sys.exit(1)

def check_cli_execution():
    """Check if databricks-sql CLI runs without errors."""
    result = subprocess.run(
        ["databricks-sql", "--help"],
        capture_output=True,
        text=True
    )
    if "Usage: databricks-sql [OPTIONS] COMMAND" in result.stdout:
        print("[OK] databricks-sql CLI is working.")
    else:
        print("[ERROR] databricks-sql CLI command failed.")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        sys.exit(1)

if __name__ == "__main__":
    check_pip_installation()
    check_python_import()
    check_cli_execution()
    print("[SUCCESS] All checks passed!")
