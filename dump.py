import subprocess
import sys
import json
import tempfile
import os
import uuid

def run_command(command):
    """Run a shell command and return its output or error."""
    try:
        return subprocess.check_output(command, shell=True, text=True).strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.strip()}"

def save_to_tempfile(content):
    """Save content to a temporary file and return the filename."""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(content.encode())
    temp_file.close()
    return temp_file.name

def compare_content(old_content, new_content, section_title):
    """Compare two sets of content and return differences as a list."""
    if not old_content.strip() and not new_content.strip():
        return []

    old_lines = set(old_content.splitlines())
    new_lines = set(new_content.splitlines())
    diff = new_lines - old_lines

    if diff:
        return [f"### {section_title}\n"] + [f"- {line}" for line in diff]
    return []

def generate_report(report_sections):
    """Generate a Markdown report with all detected differences."""
    report_file = "docker_image_comparison_report.md"
    with open(report_file, "w") as f:
        f.write("# Docker Image Comparison Report\n\n")
        f.write(f"**Old Image:** `{sys.argv[1]}`\n\n")
        f.write(f"**New Image:** `{sys.argv[2]}`\n\n")

        if any(report_sections):
            for section in report_sections:
                f.write("\n".join(section) + "\n\n")
        else:
            f.write("No significant differences found.\n")

    print(f"\n✅ Report saved as `{report_file}`")

def compare_docker_images(image1, image2):
    """Compare two Docker images and generate a detailed report."""
    print(f"[*] Pulling images {image1} and {image2} to ensure the latest versions...")
    subprocess.run(f"docker pull {image1}", shell=True)
    subprocess.run(f"docker pull {image2}", shell=True)

    # Generate unique container names
    container1, container2 = f"compare_{uuid.uuid4().hex[:8]}", f"compare_{uuid.uuid4().hex[:8]}"
    
    print(f"\n[*] Creating temporary containers: {container1} & {container2}...")
    subprocess.run(f"docker create --name {container1} {image1}", shell=True)
    subprocess.run(f"docker create --name {container2} {image2}", shell=True)

    report_sections = []

    # 1. Compare File System
    print("\n[*] Comparing File System Changes...")
    diff1 = run_command(f"docker diff {container1}")
    diff2 = run_command(f"docker diff {container2}")
    report_sections.append(compare_content(diff1, diff2, "File System Changes"))

    # 2. Compare Installed Packages
    print("\n[*] Comparing Installed Packages...")
    package_cmd_deb = "dpkg -l | awk '{print $2}' | sort"
    package_cmd_rpm = "rpm -qa --qf '%{NAME}\n' | sort"

    package_cmd = package_cmd_deb if "debian" in image1.lower() or "ubuntu" in image1.lower() else package_cmd_rpm

    pkgs1 = run_command(f"docker run --rm {image1} sh -c '{package_cmd}'")
    pkgs2 = run_command(f"docker run --rm {image2} sh -c '{package_cmd}'")
    report_sections.append(compare_content(pkgs1, pkgs2, "Installed Packages"))

    # 3. Compare Environment Variables
    print("\n[*] Comparing Environment Variables...")
    env1 = run_command(f"docker run --rm {image1} env")
    env2 = run_command(f"docker run --rm {image2} env")
    report_sections.append(compare_content(env1, env2, "Environment Variables"))

    # 4. Compare Image Layers
    print("\n[*] Comparing Image Layers...")
    layers1 = run_command(f"docker history --no-trunc {image1}")
    layers2 = run_command(f"docker history --no-trunc {image2}")
    report_sections.append(compare_content(layers1, layers2, "Image Layers"))

    # 5. Compare Metadata
    print("\n[*] Comparing Image Metadata...")
    metadata1 = json.loads(run_command(f"docker inspect {image1}"))[0]
    metadata2 = json.loads(run_command(f"docker inspect {image2}"))[0]
    metadata_diff = {key: metadata2[key] for key in metadata2 if metadata1.get(key) != metadata2.get(key)}
    if metadata_diff:
        report_sections.append(["### Image Metadata Differences"] + [f"- `{key}`: {metadata_diff[key]}" for key in metadata_diff])

    # 6. Compare Configurations
    print("\n[*] Comparing Image Configurations...")
    config1 = run_command(f"docker inspect -f '{{{{json .Config}}}}' {image1}")
    config2 = run_command(f"docker inspect -f '{{{{json .Config}}}}' {image2}")
    report_sections.append(compare_content(config1, config2, "Configuration Differences"))

    # 7. Compare Exposed Ports & Networking
    print("\n[*] Comparing Exposed Ports & Networking...")
    network1 = run_command(f"docker inspect -f '{{{{json .NetworkSettings}}}}' {image1}")
    network2 = run_command(f"docker inspect -f '{{{{json .NetworkSettings}}}}' {image2}")
    report_sections.append(compare_content(network1, network2, "Exposed Ports & Networking"))

    # 8. Compare Volumes & Mount Points
    print("\n[*] Comparing Volumes & Mount Points...")
    volumes1 = run_command(f"docker inspect -f '{{{{json .Mounts}}}}' {image1}")
    volumes2 = run_command(f"docker inspect -f '{{{{json .Mounts}}}}' {image2}")
    report_sections.append(compare_content(volumes1, volumes2, "Volumes & Mount Points"))

    # Cleanup temporary containers
    print(f"\n[*] Cleaning up temporary containers: {container1} & {container2}...")
    subprocess.run(f"docker rm {container1} {container2}", shell=True)

    # Generate final report
    generate_report(report_sections)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <old_image> <new_image>")
        sys.exit(1)

    compare_docker_images(sys.argv[1], sys.argv[2])
