def inspect_docker_image(image_name):
    """Inspects the Docker image for details like name, ID, and size."""
    metadata = {}

    # Get image size and human-readable format
    size_result = subprocess.run(["docker", "inspect", "--format", "{{.Size}}", image_name], capture_output=True, text=True)
    image_size = int(size_result.stdout.strip())
    metadata['size'] = human_readable_size(image_size)

    # Get image ID
    id_result = subprocess.run(["docker", "inspect", "--format", "{{.ID}}", image_name], capture_output=True, text=True)
    metadata['id'] = id_result.stdout.strip()

    # Get image tags
    tag_result = subprocess.run(["docker", "inspect", "--format", "{{.RepoTags}}", image_name], capture_output=True, text=True)
    metadata['tags'] = tag_result.stdout.strip()

    # Get creation date
    creation_result = subprocess.run(["docker", "inspect", "--format", "{{.Created}}", image_name], capture_output=True, text=True)
    metadata['created'] = creation_result.stdout.strip()

    # Get architecture
    arch_result = subprocess.run(["docker", "inspect", "--format", "{{.Architecture}}", image_name], capture_output=True, text=True)
    metadata['architecture'] = arch_result.stdout.strip()

    # Get environment variables
    env_result = subprocess.run(["docker", "inspect", "--format", "{{.Config.Env}}", image_name], capture_output=True, text=True)
    metadata['env_variables'] = env_result.stdout.strip()

    # Get entrypoint and CMD
    entrypoint_result = subprocess.run(["docker", "inspect", "--format", "{{.Config.Entrypoint}}", image_name], capture_output=True, text=True)
    cmd_result = subprocess.run(["docker", "inspect", "--format", "{{.Config.Cmd}}", image_name], capture_output=True, text=True)
    metadata['entrypoint'] = entrypoint_result.stdout.strip()
    metadata['cmd'] = cmd_result.stdout.strip()

    # Get exposed ports
    exposed_ports_result = subprocess.run(["docker", "inspect", "--format", "{{.Config.ExposedPorts}}", image_name], capture_output=True, text=True)
    metadata['exposed_ports'] = exposed_ports_result.stdout.strip()

    # Get volumes
    volumes_result = subprocess.run(["docker", "inspect", "--format", "{{.Config.Volumes}}", image_name], capture_output=True, text=True)
    metadata['volumes'] = volumes_result.stdout.strip()

    # Get health check configuration
    healthcheck_result = subprocess.run(["docker", "inspect", "--format", "{{.Config.Healthcheck}}", image_name], capture_output=True, text=True)
    metadata['healthcheck'] = healthcheck_result.stdout.strip()

    # Output metadata to a file
    with open(DOCKER_METADATA_FILE, 'w') as outfile:
        json.dump(metadata, outfile, indent=4)

    print(f"Metadata saved at {DOCKER_METADATA_FILE}")
