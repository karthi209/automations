import subprocess
import sys
import json
import tempfile
import os

def run_command(command):
    """Run a shell command and return its output."""
    try:
        return subprocess.check_output(command, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {command}\n{e.output}"

def compare_files(file1, file2, description):
    """Compare two files and print differences."""
    with open(file1, "r") as f1, open(file2, "r") as f2:
        content1, content2 = f1.readlines(), f2.readlines()

    diff = set(content2) - set(content1)
    if diff:
        print(f"\n[+] {description} Differences:")
        for line in diff:
            print(line.strip())

def save_to_tempfile(content):
    """Save content to a temporary file and return the filename."""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(content.encode())
    temp_file.close()
    return temp_file.name

def compare_docker_images(image1, image2):
    print(f"Comparing {image1} with {image2}...\n")

    # 1. Compare File System
    print("[*] Comparing File System Changes...")
    subprocess.run(f"docker create --name temp1 {image1}", shell=True)
    subprocess.run(f"docker create --name temp2 {image2}", shell=True)
    
    diff1 = run_command("docker diff temp1")
    diff2 = run_command("docker diff temp2")
    
    diff_file1, diff_file2 = save_to_tempfile(diff1), save_to_tempfile(diff2)
    compare_files(diff_file1, diff_file2, "File System")
    
    subprocess.run("docker rm temp1 temp2", shell=True)

    # 2. Compare Installed Packages
    print("\n[*] Comparing Installed Packages...")
    package_cmd_deb = "dpkg -l | awk '{print $2}' | sort"
    package_cmd_rpm = "rpm -qa --qf '%{NAME}\n' | sort"

    package_cmd = package_cmd_deb if "debian" in image1.lower() or "ubuntu" in image1.lower() else package_cmd_rpm

    pkgs1 = run_command(f"docker run --rm {image1} sh -c '{package_cmd}'")
    pkgs2 = run_command(f"docker run --rm {image2} sh -c '{package_cmd}'")
    
    pkgs_file1, pkgs_file2 = save_to_tempfile(pkgs1), save_to_tempfile(pkgs2)
    compare_files(pkgs_file1, pkgs_file2, "Installed Packages")

    # 3. Compare Environment Variables
    print("\n[*] Comparing Environment Variables...")
    env1 = run_command(f"docker run --rm {image1} env")
    env2 = run_command(f"docker run --rm {image2} env")

    env_file1, env_file2 = save_to_tempfile(env1), save_to_tempfile(env2)
    compare_files(env_file1, env_file2, "Environment Variables")

    # 4. Compare Image Layers
    print("\n[*] Comparing Image Layers...")
    layers1 = run_command(f"docker history --no-trunc {image1}")
    layers2 = run_command(f"docker history --no-trunc {image2}")

    layers_file1, layers_file2 = save_to_tempfile(layers1), save_to_tempfile(layers2)
    compare_files(layers_file1, layers_file2, "Image Layers")

    # 5. Compare Metadata
    print("\n[*] Comparing Image Metadata...")
    metadata1 = json.loads(run_command(f"docker inspect {image1}"))
    metadata2 = json.loads(run_command(f"docker inspect {image2}"))

    metadata_diff = {key: metadata2[0][key] for key in metadata2[0] if metadata1[0].get(key) != metadata2[0].get(key)}
    if metadata_diff:
        print("\n[+] Metadata Differences:")
        print(json.dumps(metadata_diff, indent=4))

    # Cleanup temp files
    for temp_file in [diff_file1, diff_file2, pkgs_file1, pkgs_file2, env_file1, env_file2, layers_file1, layers_file2]:
        os.remove(temp_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <old_image> <new_image>")
        sys.exit(1)

    compare_docker_images(sys.argv[1], sys.argv[2])
