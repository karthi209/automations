import subprocess
import os
import json
import docker
from pathlib import Path
from typing import Dict, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DockerTestRunner:
    """Manages Docker container operations and test execution."""
    
    def __init__(
        self,
        docker_image_name: str,
        test_files_dir: str,
        container_dir: str = '/tmp/test_tools'
    ):
        """
        Initialize the Docker test runner with configuration parameters.
        
        Args:
            docker_image_name: Name of the Docker image to use
            test_files_dir: Local directory containing test files
            container_dir: Directory inside container for test files
        """
        self.docker_image_name = docker_image_name
        self.test_files_dir = Path(test_files_dir)
        self.container_dir = Path(container_dir)
        self.container_name = f"test_container_{os.urandom(4).hex()}"
        
        # Define paths for reports and artifacts
        self.paths = {
            'test_report': self.container_dir / 'test_report.json',
            'tool_version': self.container_dir / 'tool_version.json',
            'output_report': self.container_dir / 'final_report.md',
            'venv': self.container_dir / 'venv'
        }
        
        # Status indicators for reports
        self.SUCCESS_ICON = "✅"
        self.FAILURE_ICON = "❌"
        
        # Initialize Docker client
        try:
            self.client = docker.from_env()
        except docker.errors.DockerException as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            raise

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

    def setup_virtual_environment(self, container: docker.models.containers.Container) -> bool:
        """
        Set up Python virtual environment in the container.
        
        Args:
            container: Docker container instance
            
        Returns:
            bool: True if setup successful, False otherwise
        """
        try:
            # Create virtual environment
            exit_code, _ = self._execute_container_command(
                container,
                f"python3 -m venv {self.paths['venv']}"
            )
            if exit_code != 0:
                return False
                
            # Install required packages
            exit_code, _ = self._execute_container_command(
                container,
                f"source {self.paths['venv']}/bin/activate && "
                "pip install pytest pytest-json-report"
            )
            return exit_code == 0
            
        except Exception as e:
            logger.error(f"Failed to set up virtual environment: {e}")
            return False

    def run_tests(self, container: docker.models.containers.Container) -> Optional[Path]:
        """
        Run pytest inside the container and generate JSON report.
        
        Args:
            container: Docker container instance
            
        Returns:
            Optional[Path]: Path to test report if successful, None otherwise
        """
        try:
            command = (
                f"source {self.paths['venv']}/bin/activate && "
                f"PYTHONPATH={self.container_dir} pytest "
                f"--json-report --json-report-file={self.paths['test_report']}"
            )
            
            exit_code, output = self._execute_container_command(container, command)
            
            logger.info("Pytest output:")
            logger.info(output)
            
            return self.paths['test_report'] if exit_code == 0 else None
            
        except Exception as e:
            logger.error(f"Failed to run tests: {e}")
            return None

    @staticmethod
    def load_json(file_path: Path) -> Dict:
        """
        Load and parse a JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Dict: Parsed JSON data or empty dict if failed
        """
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON from {file_path}")
        return {}

    @staticmethod
    def extract_tool_name(nodeid: str) -> str:
        """
        Extract tool name from pytest nodeid.
        
        Args:
            nodeid: pytest node identifier
            
        Returns:
            str: Extracted tool name or 'Unknown'
        """
        try:
            parts = nodeid.split('/')
            if len(parts) > 1:
                return parts[1].split('.')[0]
        except Exception as e:
            logger.error(f"Failed to extract tool name from {nodeid}: {e}")
        return "Unknown"

    def generate_markdown(self, test_report: Dict, tool_versions: Dict) -> None:
        """
        Generate markdown report from test results and tool versions.
        
        Args:
            test_report: Test results dictionary
            tool_versions: Tool versions dictionary
        """
        try:
            markdown = "# Test Summary Report\n\n"
            tools = {}

            # Process test results
            for test in test_report.get('tests', []):
                nodeid = test.get('nodeid', '')
                outcome = test.get('outcome', 'unknown')
                tool_name = self.extract_tool_name(nodeid)
                test_name = nodeid.split('::')[-1]

                if tool_name not in tools:
                    tools[tool_name] = {
                        "version": tool_versions.get(tool_name, "Version not found"),
                        "tests": []
                    }

                icon = self.SUCCESS_ICON if outcome == 'passed' else self.FAILURE_ICON
                tools[tool_name]['tests'].append(f"{test_name} : {icon} ({outcome})")

            # Generate markdown content
            for tool, details in tools.items():
                markdown += f"## {tool} (Version: {details['version']})\n"
                for test_result in details['tests']:
                    markdown += f"- {test_result}\n"
                markdown += "\n"

            # Write markdown file
            with open(self.paths['output_report'], 'w') as file:
                file.write(markdown)

            logger.info(f"Markdown report saved to {self.paths['output_report']}")
            
        except Exception as e:
            logger.error(f"Failed to generate markdown report: {e}")

    def run(self) -> None:
        """Execute the complete test suite in a Docker container."""
        container = None
        try:
            # Start container
            container = self.client.containers.run(
                self.docker_image_name,
                name=self.container_name,
                detach=True,
                volumes={
                    str(self.test_files_dir): {
                        'bind': str(self.container_dir),
                        'mode': 'rw'
                    }
                },
                environment=["PYTHONPATH=/tmp/test_tools"],
            )
            logger.info(f"Container {self.container_name} started successfully")

            # Setup virtual environment
            if not self.setup_virtual_environment(container):
                raise RuntimeError("Failed to set up virtual environment")

            # Run tests
            test_report_path = self.run_tests(container)
            if not test_report_path:
                raise RuntimeError("Failed to generate test report")

            # Copy reports from container
            with open(self.paths['test_report'], 'wb') as f:
                f.write(container.exec_run(f"cat {test_report_path}").output)

            with open(self.paths['tool_version'], 'wb') as f:
                f.write(container.exec_run(f"cat {self.paths['tool_version']}").output)

            # Generate final report
            test_report = self.load_json(self.paths['test_report'])
            tool_versions = self.load_json(self.paths['tool_version'])

            if test_report and tool_versions:
                self.generate_markdown(test_report, tool_versions)

        except Exception as e:
            logger.error(f"Test execution failed: {e}")
            raise
        finally:
            if container:
                try:
                    container.stop()
                    container.remove()
                    logger.info(f"Container {self.container_name} cleaned up")
                except Exception as e:
                    logger.error(f"Failed to clean up container: {e}")

if __name__ == "__main__":
    # Example usage
    runner = DockerTestRunner(
        docker_image_name="your-docker-image-name",
        test_files_dir="/path/to/test_files"
    )
    runner.run()
