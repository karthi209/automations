def _execute_container_command(
    self,
    container: docker.models.containers.Container,
    command: str
) -> tuple[int, str]:
    """Execute a command in the container and return results."""
    result = container.exec_run(command)
    exit_code, output = result  # Unpack the result tuple properly
    output = output.decode('utf-8')  # Decode the byte string to a regular string
    
    if exit_code != 0:
        logger.warning(f"Command '{command}' failed with exit code {exit_code}")
        logger.warning(f"Output: {output}")
    return exit_code, output
