import pytest
import os

@pytest.mark.parametrize("filepath", [
    "/etc/passwd",  # Example: Check if /etc/passwd exists
])
def test_file_exists(filepath):
    assert os.path.exists(filepath), f"File {filepath} does not exist"
