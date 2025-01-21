import os
import subprocess
import pytest


# List of alternatives to test
JAVA_ALTERNATIVES = [
    "java",
    "javac",
    "keytool",
    "jar"
]


@pytest.mark.parametrize("alternative", JAVA_ALTERNATIVES)
def test_alternative_exists(alternative):
    """Check if the symlink for the given alternative exists in /etc/alternatives."""
    symlink_path = f"/etc/alternatives/{alternative}"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."
    assert os.path.exists(os.readlink(symlink_path)), f"Target for {symlink_path} does not exist."


@pytest.mark.parametrize("alternative", JAVA_ALTERNATIVES)
def test_alternative_points_to_correct_version(alternative):
    """Check if the alternative points to the correct Java version."""
    symlink_path = f"/etc/alternatives/{alternative}"
    target_path = os.readlink(symlink_path)  # Resolve the symlink
    assert "java" in target_path.lower(), f"{symlink_path} does not point to a Java binary."
    assert os.path.exists(target_path), f"The target binary {target_path} does not exist."


@pytest.mark.parametrize("alternative", JAVA_ALTERNATIVES)
def test_alternative_executable(alternative):
    """Check if the alternative executable runs correctly."""
    try:
        output = subprocess.check_output([alternative, "-version"], stderr=subprocess.STDOUT, text=True)
        assert "java" in output.lower(), f"{alternative} -version did not return expected output."
    except FileNotFoundError:
        pytest.fail(f"{alternative} is not executable or not found in PATH.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Error while running {alternative}: {e}")
