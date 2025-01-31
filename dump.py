import os
import pytest

def test_home_env():
    expected_home_paths = ["/apps/runner", "/app/jenkins-agent"]

    assert "HOME" in os.environ, "HOME environment variable is not set."
    
    actual_home = os.environ["HOME"]
    assert actual_home in expected_home_paths, (
        f"HOME is set to {actual_home}, but expected one of {expected_home_paths}"
    )
