#!/bin/bash

molecule converge

# Array of instance names and associated users
declare -A instance_users=(
  ["instance_git"]="git"
  ["instance_git_scale_set"]="jenkins"
)

for instance in "${!instance_users[@]}"; do
  user="${instance_users[$instance]}"
  echo "Processing instance: $instance with user: $user"

  # Copy test file and adjust ownership
  if docker cp --help | grep -q -- "--chown"; then
    docker cp --chown="$user:$user" tests/test_git.py "$instance:/tmp/test_git.py"
  else
    docker cp tests/test_git.py "$instance:/tmp/test_git.py"
    docker exec "$instance" chown "$user:$user" /tmp/test_git.py
  fi
  docker exec "$instance" chmod +x /tmp/test_git.py

  # Create venv and install pytest
  docker exec -u "$user" "$instance" python -m venv /tmp/venv
  docker exec -u "$user" "$instance" bash -c "source /tmp/venv/bin/activate && pip install pytest"

  # Run test with activated venv
  docker exec -u "$user" "$instance" bash -c "source /tmp/venv/bin/activate && pytest /tmp/test_git.py"

  echo "Completed instance: $instance"
done

molecule destroy