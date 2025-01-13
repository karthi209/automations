import argparse
import docker
import os
import sys
import tarfile
from io import BytesIO

def create_tar_from_file(src_path):
    """Create a tar archive from the given file."""
    tar_stream = BytesIO()
    with tarfile.open(fileobj=tar_stream, mode="w") as tar:
        arcname = os.path.basename(src_path)
        tar.add(src_path, arcname=arcname)
    tar_stream.seek(0)
    return tar_stream

def copy_file_to_container(container, src_path, dest_path):
    """Copy a file to the running container."""
    # Make sure the file exists
    if not os.path.isfile(src_path):
        raise Exception(f"Source file {src_path} does not exist")
    
    # Create tar stream for the file
    tar_stream = create_tar_from_file(src_path)
    
    # Put the tar stream in the container at the specified path
    try:
        print(f"Copying {src_path} to {dest_path}")
        container.put_archive(os.path.dirname(dest_path), tar_stream)
    except Exception as e:
        print(f"Error copying file {src_path} to container: {e}")
        sys.exit(1)

def run_tests_in_image(image_name, test_files):
    """Run test scripts inside the specified Docker image."""
    client = docker.from_env()
    try:
        print(f"Pulling image: {image_name}")
        client.images.pull(image_name)

        print(f"Starting container for image: {image_name}")
        container = client.containers.run(
            image_name,
            command="tail -f /dev/null",  # Keep the container running
            detach=True,
        )

        try:
            # Copy each test file from local to container
            for local_path, container_path in test_files.items():
                print(f"Copying {local_path} to {container_path} in container")
                copy_file_to_container(container, local_path, container_path)

            print("Running test script inside container...")
            exit_code, output = container.exec_run("python3 /test_installations.py")
            print(output.decode())
            if exit_code != 0:
                raise Exception("Test script failed.")
        finally:
            print(f"Stopping container for image: {image_name}")
            container.stop()
            container.remove()

    except Exception as e:
        print(f"Error testing image {image_name}: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Test Docker image installations.")
    parser.add_argument("image", help="The Docker image to test.")
    parser.add_argument(
        "--test-files", 
        nargs="+", 
        help="List of test files to copy into the container in the format 'local_path:container_path'.",
        required=True
    )
    args = parser.parse_args()

    # Parse test files into a dictionary
    test_files = {}
    for pair in args.test_files:
        local, container = pair.split(":")
        test_files[local] = container

    # Run tests
    run_tests_in_image(args.image, test_files)


if __name__ == "__main__":
    main()
