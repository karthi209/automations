def inspect_docker_image(image_name):
    """Inspects the Docker image for details like name, ID, and size."""
    inspect_cmd = ["docker", "inspect", "--format", "{{json .}}", image_name]
    result = subprocess.run(inspect_cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        try:
            # Print raw output for debugging
            print("Raw docker inspect output:", result.stdout)
            
            # Parse the JSON output
            image_info = json.loads(result.stdout)

            # If the result is a list and has one or more items, proceed
            if isinstance(image_info, list) and len(image_info) > 0:
                image_details = image_info[0]  # Extract the first image object
                print(f"Image ID: {image_details['Id']}")
                print(f"Image Name: {image_details['RepoTags'][0]}")
                print(f"Image Size: {image_details['Size']} bytes")
                print(f"Created: {image_details['Created']}")
                return image_details
            else:
                print(f"Unexpected format: The output is not a list or is empty")
                sys.exit(1)
        
        except json.JSONDecodeError as e:
            print(f"Error parsing Docker inspect output: {e}")
            sys.exit(1)
    else:
        print(f"Failed to inspect image: {image_name}")
        sys.exit(1)
