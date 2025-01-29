#!/bin/bash

cd ..
molecule converge

tool="git"
test_file="test_${tool}.py"

# Array of instance names and associated users
declare -A instance_users=(
    ["instance_git"]="jenkins"
    ["instance_git_scale_set"]="runner"
)

for instance in "${!instance_users[@]}"; do
    user="${instance_users[$instance]}"
    echo "Processing instance: $instance with user: $user"

    # Copy test file and adjust ownership
    if docker cp --help | grep -q -- "--chown"; then
        docker cp --chown="$user:$user" "tests/$test_file" "$instance:/tmp/$test_file"
    else
        docker cp "tests/$test_file" "$instance:/tmp/$test_file"
        docker exec "$instance" chown "$user:$user" "/tmp/$test_file"
    fi

    docker exec "$instance" chmod +x "/tmp/$test_file"

    # Create venv and install pytest
    docker exec -u "$user" "$instance" python -m venv /tmp/venv
    docker exec -u "$user" "$instance" bash -c "source /tmp/venv/bin/activate && pip install pytest"

    # Run test with activated venv
    docker exec -u "$user" "$instance" bash -c "source /tmp/venv/bin/activate && pytest /tmp/$test_file"

    echo "Completed instance: $instance"
done

molecule destroy
