import subprocess
import os
import pytest

def test_gradle_build():
    try:
        # Create a simple gradle project structure for the test
        project_dir = 'test-project'
        
        # Make sure the test project directory is created
        os.makedirs(project_dir, exist_ok=True)

        # Create the settings.gradle file
        with open(os.path.join(project_dir, 'settings.gradle'), 'w') as f:
            f.write('rootProject.name = "test-project"')

        # Create a simple build.gradle file
        with open(os.path.join(project_dir, 'build.gradle'), 'w') as f:
            f.write('task hello { doLast { println "Hello, Gradle!" } }')

        # Run gradle tasks inside the project directory
        result = subprocess.run(['gradle', 'tasks'], capture_output=True, text=True, check=True, cwd=project_dir)
        
        # Assert that the "hello" task is listed
        assert "hello" in result.stdout, f"Expected 'hello' task but got: {result.stdout}"

    except subprocess.CalledProcessError as e:
        pytest.fail(f"Gradle build failed: {e.stderr}")
    finally:
        # Clean up: Remove the test project folder after the test
        subprocess.run(['rm', '-rf', project_dir], capture_output=True, text=True)

