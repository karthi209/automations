def _execute_container_command(
    self,
    container: docker.models.containers.Container,
    command: str
) -> tuple[int, str]:
    """Execute a command in the container and return results."""
    try:
        result = container.exec_run(command)
        # Ensure that result is a tuple
        if isinstance(result, tuple) and len(result) == 2:
            exit_code, output = result
            output = output.decode('utf-8')  # Decode from bytes to string
            if exit_code != 0:
                logger.warning(f"Command '{command}' failed with exit code {exit_code}")
                logger.warning(f"Output: {output}")
            return exit_code, output
        else:
            raise ValueError(f"Unexpected result format: {result}")
    except Exception as e:
        logger.error(f"Failed to execute command '{command}': {e}")
        return 1, str(e)  # Return error code and message
