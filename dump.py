import sys
import time
import subprocess
from docker_utils import run_docker_tests
from metadata_utils import save_metadata
from tool_check_script import get_tool_versions
from subprocess_utils import safe_subprocess_call

def main(image_name):
    # Step 1: Ensure the Docker image is pulled or exists locally
    run_docker_tests(image_name)

    # Step 2: Get image metadata and save it
    metadata = get_image_metadata(image_name)
    save_metadata(image_name, metadata)

    # Step 3: Check the versions of the tools inside the container
    get_tool_versions()

    # Step 4: Check the installed packages inside the container
    # You can add additional functionality here to ensure package check is done

    print(f"Tests and checks completed for image: {image_name}")


def get_image_metadata(image_name):
    print("🔍 Retrieving Docker image metadata...")

    # Inspect the Docker image to retrieve metadata
    inspect_cmd = f"docker inspect {image_name}"
    result = subprocess.run(inspect_cmd, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Failed to inspect image {image_name}: {result.stderr}")
        sys.exit(1)

    image_info = json.loads(result.stdout)[0]  # Get first (and only) result

    # Get image size in MB
    size_cmd = f"docker images --format '{{{{.Size}}}}' {image_name}"
    size_result = subprocess.run(size_cmd, shell=True, capture_output=True, text=True)

    metadata = {
        "Image_ID": image_info["Id"],
        "Repo_Tags": image_info.get("RepoTags", []),
        "Created": image_info["Created"],
        "Size": size_result.stdout.strip(),
        "Architecture": image_info.get("Architecture", "unknown"),
        "OS": image_info.get("Os", "unknown"),
        "Digest": image_info.get("RepoDigests", [])
    }

    return metadata


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_manager.py <image_name>")
        sys.exit(1)

    image_name = sys.argv[1]
    main(image_name)
