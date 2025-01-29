def test_gradle_build():
    try:
        # Create a simple gradle project structure for the test
        subprocess.run(['mkdir', '-p', 'test-project'])
        subprocess.run(['echo', 'rootProject.name = "test-project"', '>', 'test-project/settings.gradle'])
        subprocess.run(['echo', 'task hello { doLast { println "Hello, Gradle!" } }', '>', 'test-project/build.gradle'])

        # Run gradle tasks in the created project directory
        result = subprocess.run(['gradle', 'tasks'], capture_output=True, text=True, check=True, cwd='test-project')
        assert "hello" in result.stdout, f"Expected 'hello' task but got: {result.stdout}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Gradle build failed: {e.stderr}")
