import subprocess
import json
import sys
import time
import os
from datetime import datetime
from pathlib import Path
import hashlib
from typing import Dict, Any

# Constants
TEMP_DIR = "/tmp/test_tools"
DEFAULT_TIMEOUT = 300  # 5 minutes
CONTAINER_MEMORY_LIMIT = "1g"
CONTAINER_CPU_LIMIT = "1"
OUTPUT_DIR = Path("./docker_analysis")

class DockerAnalysisError(Exception):
    """Custom exception for Docker analysis errors"""
    pass

def create_safe_directory(path: Path) -> None:
    """Create directory with secure permissions"""
    path.mkdir(parents=True, exist_ok=True)
    os.chmod(path, 0o755)  # rwxr-xr-x

def safe_subprocess_call(command: str, description: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """Executes a subprocess command and logs errors if it fails."""
    try:
        print(f"🔹 Running: {description}...")
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode != 0:
            raise DockerAnalysisError(f"Error during {description}: {result.stderr}")
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        raise DockerAnalysisError(f"Timeout ({timeout}s) exceeded during {description}")
    except Exception as e:
        raise DockerAnalysisError(f"Failed during {description}: {str(e)}")

def write_json_safely(data: Dict[str, Any], filepath: Path) -> None:
    """Write JSON data to file with error handling"""
    try:
        with filepath.open('w') as f:
            json.dump(data, f, indent=2, sort_keys=True)
    except IOError as e:
        raise DockerAnalysisError(f"Error writing to {filepath}: {e}")

def read_json_safely(filepath: Path) -> Dict[str, Any]:
    """Read JSON data from file with error handling"""
    try:
        with filepath.open('r') as f:
            return json.load(f)
    except IOError as e:
        raise DockerAnalysisError(f"Error reading {filepath}: {e}")

def get_image_digest(image_name: str) -> str:
    """Get Docker image digest"""
    return safe_subprocess_call(
        f"docker inspect --format='{{{{.Id}}}}' {image_name}",
        "get image digest"
    )

def analyze_docker_image(image_name: str) -> Dict[str, Any]:
    """Collect detailed Docker image information"""
    inspect_data = json.loads(safe_subprocess_call(
        f"docker inspect {image_name}",
        "inspect Docker image"
    ))
    
    layers = safe_subprocess_call(
        f"docker history --no-trunc --format '{{{{.CreatedBy}}}}' {image_name}",
        "get image layers"
    ).split('\n')
    
    return {
        "digest": get_image_digest(image_name),
        "created": inspect_data[0]["Created"],
        "architecture": inspect_data[0]["Architecture"],
        "os": inspect_data[0]["Os"],
        "layers": [hashlib.sha256(layer.encode()).hexdigest() for layer in layers],
        "env_vars": inspect_data[0].get("Config", {}).get("Env", []),
        "exposed_ports": list(inspect_data[0].get("Config", {}).get("ExposedPorts", {}).keys()),
        "labels": inspect_data[0].get("Config", {}).get("Labels", {}),
        "size": inspect_data[0]["Size"],
        "virtual_size": inspect_data[0]["VirtualSize"]
    }

def run_docker_tests(image_name: str) -> None:
    """Run comprehensive Docker image analysis"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_tag = image_name.replace(":", "_").replace("/", "_")
    analysis_dir = OUTPUT_DIR / f"{image_tag}_{timestamp}"
    create_safe_directory(analysis_dir)
    
    container_name = f"test-container-{int(time.time())}"
    
    try:
        # Check if image exists locally
        if not safe_subprocess_call(f"docker images -q {image_name}", "check image existence"):
            print(f"⚠️ Image '{image_name}' not found locally, pulling from remote...")
            safe_subprocess_call(f"docker pull {image_name}", "pull Docker image")

        # Collect image analysis before running container
        image_info = analyze_docker_image(image_name)
        write_json_safely(image_info, analysis_dir / "image_analysis.json")

        # Start container with resource limits
        safe_subprocess_call(
            f"docker run -d --user runner "
            f"--memory={CONTAINER_MEMORY_LIMIT} --cpus={CONTAINER_CPU_LIMIT} "
            f"--name {container_name} {image_name} tail -f /dev/null",
            "start Docker container"
        )

        # Create secure temporary directory
        safe_subprocess_call(
            f"docker exec {container_name} mkdir -p {TEMP_DIR}",
            "prepare temporary directory"
        )
        safe_subprocess_call(
            f"docker exec {container_name} chmod 750 {TEMP_DIR}",
            "set secure permissions"
        )

        # Copy and validate tool version config
        config_path = Path("./tool_version_config.json")
        if not config_path.exists():
            raise DockerAnalysisError("tool_version_config.json not found")
        
        tool_config = read_json_safely(config_path)
        if not isinstance(tool_config, dict):
            raise DockerAnalysisError("Invalid tool_version_config.json format")

        safe_subprocess_call(
            f"docker cp {config_path} {container_name}:{TEMP_DIR}/tool_version_config.json",
            "copy tool version config"
        )

        # Collect system information
        system_info_script = """
import platform
import os
import json
import subprocess

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except:
        return "N/A"

info = {
    "hostname": platform.node(),
    "platform": platform.platform(),
    "python_version": platform.python_version(),
    "cpu_info": run_cmd("cat /proc/cpuinfo | grep 'model name' | head -1"),
    "memory_info": run_cmd("free -h"),
    "disk_usage": run_cmd("df -h"),
    "network_interfaces": run_cmd("ip addr show"),
    "installed_packages": run_cmd("rpm -qa"),
    "environment_variables": dict(os.environ),
    "system_users": run_cmd("cat /etc/passwd"),
    "running_services": run_cmd("systemctl list-units --type=service"),
    "open_ports": run_cmd("netstat -tulpn"),
    "loaded_kernel_modules": run_cmd("lsmod"),
    "mounted_filesystems": run_cmd("mount"),
}

with open('/tmp/test_tools/system_info.json', 'w') as f:
    json.dump(info, f, indent=2)
"""
        # Execute system info collection
        safe_subprocess_call(
            f"docker exec {container_name} python3 -c '{system_info_script}'",
            "collect system information"
        )

        # Copy results back to host
        for filename in ["system_info.json"]:
            safe_subprocess_call(
                f"docker cp {container_name}:{TEMP_DIR}/{filename} {analysis_dir}/{filename}",
                f"copy {filename}"
            )

        print(f"\n✅ Analysis complete! Results saved in: {analysis_dir}")
        
    except DockerAnalysisError as e:
        print(f"\n❌ Analysis failed: {str(e)}")
        sys.exit(1)
    finally:
        # Cleanup
        try:
            safe_subprocess_call(f"docker stop {container_name}", "stop container", timeout=30)
            safe_subprocess_call(f"docker rm {container_name}", "remove container", timeout=30)
        except DockerAnalysisError as e:
            print(f"⚠️ Cleanup error: {str(e)}")

def compare_analyses(dir1: Path, dir2: Path) -> Dict[str, Any]:
    """Compare two Docker image analyses"""
    try:
        analysis1 = read_json_safely(dir1 / "image_analysis.json")
        analysis2 = read_json_safely(dir2 / "image_analysis.json")
        
        comparison = {
            "timestamp": datetime.now().isoformat(),
            "image1": dir1.name,
            "image2": dir2.name,
            "differences": {
                "layers_added": [l for l in analysis2["layers"] if l not in analysis1["layers"]],
                "layers_removed": [l for l in analysis1["layers"] if l not in analysis2["layers"]],
                "env_vars_added": [e for e in analysis2["env_vars"] if e not in analysis1["env_vars"]],
                "env_vars_removed": [e for e in analysis1["env_vars"] if e not in analysis2["env_vars"]],
                "ports_added": [p for p in analysis2["exposed_ports"] if p not in analysis1["exposed_ports"]],
                "ports_removed": [p for p in analysis1["exposed_ports"] if p not in analysis2["exposed_ports"]],
                "size_diff": analysis2["size"] - analysis1["size"]
            }
        }
        
        return comparison
    except Exception as e:
        raise DockerAnalysisError(f"Error comparing analyses: {str(e)}")

if __name__ == '__main__':
    if len(sys.argv) not in [2, 4]:
        print("Usage:")
        print("  Analyze single image: python script.py <docker_image_name>")
        print("  Compare two analyses: python script.py --compare <analysis_dir1> <analysis_dir2>")
        sys.exit(1)

    try:
        if sys.argv[1] == "--compare":
            if len(sys.argv) != 4:
                raise DockerAnalysisError("Missing analysis directories for comparison")
            comparison = compare_analyses(Path(sys.argv[2]), Path(sys.argv[3]))
            output_file = OUTPUT_DIR / f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            write_json_safely(comparison, output_file)
            print(f"\n✅ Comparison saved to: {output_file}")
        else:
            run_docker_tests(sys.argv[1])
    except DockerAnalysisError as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
