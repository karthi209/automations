import docker

def test_image(image_name, script_path):
    client = docker.from_env()
    
    print(f"Pulling image: {image_name}...")
    client.images.pull(image_name)
    
    print(f"Running tests inside the image...")
    container = client.containers.run(
        image_name,
        f"python3 {script_path}",
        volumes={
            script_path: {'bind': script_path, 'mode': 'ro'}
        },
        remove=True,
        detach=False
    )
    print(container)

if __name__ == "__main__":
    IMAGE_NAME = "your-image-name:tag"
    SCRIPT_PATH = "/test_installations.py"  # Path to the test script inside the container
    test_image(IMAGE_NAME, SCRIPT_PATH)
