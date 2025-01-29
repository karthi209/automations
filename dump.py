import pytest
import pwd
import grp
import os

@pytest.mark.parametrize("username, expected_group, expected_home", [
    ("testuser", "testgroup", "/home/testuser")
])
def test_user(username, expected_group, expected_home):
    try:
        user_info = pwd.getpwnam(username)
    except KeyError:
        pytest.fail(f"User {username} does not exist")

    assert user_info.pw_name == username, f"Expected username {username}, but got {user_info.pw_name}"
    assert user_info.pw_dir == expected_home, f"Expected home {expected_home}, but got {user_info.pw_dir}"

    # Check the primary group
    actual_group = grp.getgrgid(user_info.pw_gid).gr_name
    assert actual_group == expected_group, f"Expected group {expected_group}, but got {actual_group}"

    # Ensure user is in the group
    group_members = grp.getgrnam(expected_group).gr_mem
    assert username in group_members, f"User {username} is not in group {expected_group}"

