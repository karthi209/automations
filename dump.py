def _execute_container_command(
        self,
        container: docker.models.containers.Container,
        command: str
    ) -> tuple[int, str]:
        """
        Execute a command in the container and return results.

        Args:
            container: Docker container instance
            command: Command to execute

        Returns:
            Tuple of (exit_code, output)
        """
        result = container.exec_run(command)
        output = result.output.decode('utf-8')

        if result.exit_code != 0:
            logger.warning(f"Command '{command}' failed with exit code {result.exit_code}")
            logger.warning(f"Output: {output}")

        return result.exit_code, output
