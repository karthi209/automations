import os
import stat
import pwd

def test_multiple_file_permissions_and_ownership():
    file_variants = {
        "file1.txt": {"permissions": 0o755, "owners": ["runner", "user1"]},
        "file2.txt": {"permissions": 0o755, "owners": ["runner"]},
        "file3.txt": {"permissions": 0o755, "owners": ["runner", "admin"]},
    }

    possible_directories = ["/path/to/location1", "/path/to/location2"]

    for file_name, details in file_variants.items():
        expected_permissions = details["permissions"]
        expected_owners = details["owners"]

        # Find the actual path where the file exists
        actual_path = None
        for directory in possible_directories:
            file_path = os.path.join(directory, file_name)
            if os.path.exists(file_path):
                actual_path = file_path
                break

        assert actual_path, f"{file_name} does not exist in any expected locations: {possible_directories}"

        # Get file metadata
        file_stat = os.stat(actual_path)

        # Check permissions
        actual_permissions = file_stat.st_mode & 0o777
        assert actual_permissions == expected_permissions, (
            f"File permissions for {actual_path} are {oct(actual_permissions)}, "
            f"but expected {oct(expected_permissions)}"
        )

        # Check ownership
        actual_owner = pwd.getpwuid(file_stat.st_uid).pw_name
        assert actual_owner in expected_owners, (
            f"File owner for {actual_path} is {actual_owner}, but expected one of {expected_owners}"
        )
