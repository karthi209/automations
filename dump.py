import docker
import os
import sys

def copy_file_to_container(container, src_path, dest_path):
    """Copy a file to the running container."""
    with open(src_path, 'rb') as file_data:
        container.put_archive(
            os.path.dirname(dest_path),
            data=docker.utils.tar(
                {
                    os.path.basename(dest_path): file_data.read()
                }
            ),
        )

def run_tests_in_image(image_name, test_files):
    client = docker.from_env()
    try:
        print(f"Pulling image: {image_name}")
        client.images.pull(image_name)

        print(f"Starting container for image: {image_name}")
        container = client.containers.run(
            image_name,
            command="tail -f /dev/null",
            detach=True,
        )

        try:
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


if __name__ == "__main__":
    IMAGE_NAME = "your-image-name:tag"
    TEST_FILES = {
        "test_installations.py": "/test_installations.py",
        "tools_expected.json": "/tools_expected.json",
    }

    run_tests_in_image(IMAGE_NAME, TEST_FILES)
