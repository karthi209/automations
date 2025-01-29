def test_gradle_build():
    try:
        # Run a simple Gradle build (no project, just check if it responds)
        result = subprocess.run(['gradle', 'tasks'], capture_output=True, text=True, check=True)
        assert "Available tasks" in result.stdout, f"Expected task list but got: {result.stdout}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Gradle build failed: {e.stderr}")
