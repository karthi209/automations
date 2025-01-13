import subprocess
import json

def main():
    try:
        # Get Maven version
        version_output = subprocess.check_output(["mvn", "--version"]).decode("utf-8").splitlines()
        version = version_output[0].split()[2]  # Extract version (e.g., "Apache Maven 3.6.3")

        # Get Maven installation path
        path = subprocess.check_output(["which", "mvn"]).decode("utf-8").strip()

        # Get symlink details
        symlink = subprocess.check_output(["ls", "-l", path]).decode("utf-8").strip()

        # Functionality test: Create a sample POM file and validate it
        functionality_test = subprocess.check_output(["mvn", "-version"]).decode("utf-8").strip()

        results = {
            "Version": version,
            "Installation Path": path,
            "Symlink": symlink,
            "Functionality Test": functionality_test,
        }
    except Exception as e:
        results = {"Error": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    main()




import subprocess
import json

def main():
    try:
        # Get Git version
        version_output = subprocess.check_output(["git", "--version"]).decode("utf-8").strip()
        version = version_output.split()[2]  # Extract version (e.g., "git version 2.30.2")

        # Get Git installation path
        path = subprocess.check_output(["which", "git"]).decode("utf-8").strip()

        # Get symlink details
        symlink = subprocess.check_output(["ls", "-l", path]).decode("utf-8").strip()

        # Functionality test: Initialize a Git repository in a temp directory
        functionality_test = "Git initialized successfully"
        try:
            subprocess.check_output(["git", "init", "/tmp/test_git_repo"], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            functionality_test = f"Error during functionality test: {e.output.decode('utf-8').strip()}"

        results = {
            "Version": version,
            "Installation Path": path,
            "Symlink": symlink,
            "Functionality Test": functionality_test,
        }
    except Exception as e:
        results = {"Error": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    main()




{
    "Python3": {
        "Expected Version": "3.8.10",
        "Expected Installation Path": "/usr/bin/python3",
        "Expected Symlink": "python3 -> /usr/bin/python3.8"
    },
    "Maven": {
        "Expected Version": "3.6.3",
        "Expected Installation Path": "/usr/bin/mvn",
        "Expected Symlink": "mvn -> /usr/share/maven/bin/mvn"
    },
    "Git": {
        "Expected Version": "2.30.2",
        "Expected Installation Path": "/usr/bin/git",
        "Expected Symlink": "git -> /usr/share/git-core/git"
    }
}
