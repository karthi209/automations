def test_multiple_file_permissions_and_ownership():
    files_with_details = {
        "/path/to/file1.txt": {"permissions": stat.S_IRUSR | stat.S_IWUSR, "owner": "user1"},
        "/path/to/file2.txt": {"permissions": stat.S_IRUSR | stat.S_IRGRP, "owner": "user2"},
    }
    
    for file_path, details in files_with_details.items():
        expected_permissions = details["permissions"]
        expected_owner = details["owner"]

        # Check if the file exists
        assert os.path.exists(file_path), f"File does not exist at: {file_path}"

        # Get file metadata
        file_stat = os.stat(file_path)

        # Check permissions
        actual_permissions = file_stat.st_mode & 0o777
        assert actual_permissions == expected_permissions, (
            f"File permissions for {file_path} are {oct(actual_permissions)}, "
            f"but expected {oct(expected_permissions)}"
        )

        # Check ownership
        actual_owner = pwd.getpwuid(file_stat.st_uid).pw_name
        assert actual_owner == expected_owner, (
            f"File owner for {file_path} is {actual_owner}, but expected {expected_owner}"
        )
