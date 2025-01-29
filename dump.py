import pytest
from pathlib import Path

@pytest.mark.parametrize("filepaths", [
    (Path("/app/runner/file"), Path("/app/jenkins-agent/file"))
])
def test_either_file_exists(filepaths):
    assert any(filepath.exists() for filepath in filepaths), f"Neither {filepaths[0]} nor {filepaths[1]} exists"
