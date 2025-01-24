import subprocess
import os


def test_node_version():
    """Test if Node.js is installed and get its version."""
    try:
        # Run the 'node -v' command to get the version
        result = subprocess.run(["node", "-v"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        node_version = result.stdout.strip()
        assert node_version.startswith("v"), f"Unexpected Node.js version format: {node_version}"
        print(f"Node.js version: {node_version}")
    except FileNotFoundError:
        raise AssertionError("Node.js is not installed or not in PATH.")
    except subprocess.CalledProcessError as e:
        raise AssertionError(f"Error running Node.js: {e.stderr}")


def test_node_functionality():
    """Test if Node.js can execute a simple JavaScript program."""
    # JavaScript code to test basic functionality
    js_code = """
        console.log("Node.js is working!");
        const result = [1, 2, 3].map(x => x * 2);
        console.log("Array result:", result);
    """

    try:
        # Run the JavaScript code with Node.js
        result = subprocess.run(
            ["node", "-e", js_code],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout = result.stdout.strip()
        assert "Node.js is working!" in stdout, "Node.js script did not run as expected."
        assert "Array result: [ 2, 4, 6 ]" in stdout, f"Unexpected script output: {stdout}"
        print(stdout)
    except FileNotFoundError:
        raise AssertionError("Node.js is not installed or not in PATH.")
    except subprocess.CalledProcessError as e:
        raise AssertionError(f"Error running Node.js script: {e.stderr}")
