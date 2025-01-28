#!/bin/bash

# Array of instance names
instances=("gradle_instance" "another_instance" "yet_another_instance")

# Run through each instance
for instance in "${instances[@]}"; do
  echo "Processing instance: $instance"

  # Molecule converge
  molecule converge -s "$instance"

  # Copy test file
  docker cp tests/test_gradle.py "$instance:/tmp/test_gradle.py"
  docker exec -u root "$instance" chmod +x /tmp/test_gradle.py

  # Create venv and install pytest
  docker exec "$instance" python -m venv /tmp/venv
  docker exec "$instance" bash -c "source /tmp/venv/bin/activate && pip install pytest"

  # Run test with activated venv
  docker exec "$instance" bash -c "source /tmp/venv/bin/activate && pytest /tmp/test_gradle.py"

  # Molecule destroy
  molecule destroy -s "$instance"

  echo "Completed instance: $instance"
done