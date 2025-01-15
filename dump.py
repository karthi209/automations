import requests
import time
import sys
from requests.exceptions import RequestException

def trigger_jenkins_job(job_url, username, api_token, wait_time_seconds=7200, retry_interval=10):
    
    """
    Triggers a Jenkins job and waits for its completion, then fetches the result.

    Args:
    - job_url: The full job url, including folders (e.g., 'http://jenkins-server/Folder1/Folder2/example-job')
    - username: Jenkins username
    - api_token: Jenkins API token
    - wait_time_seconds: Time to wait for the job to complete (default: 7200 seconds = 2 hours)
    - retry_interval: Interval between reties (default: 60 seconds)

    Returns:
    - Triggers a Jenkins job and waits for its completion, then fetches the result.
    """
    try:
        # Trigger the job
        response = requests.post(
            f"{job_url}/build",
            auth=(username, api_token),
            timeout=10
        )
        response.raise_for_status()

    except RequestException as e:
        print(f"Failed to trigger Jenkins job: {e}")
        return {"status": "error", "message": str(e)}

    print(f"Jenkins job triggered successfully.")
    
    time.sleep(15)

    # Wait for the job to complete (with retries)
    start_time = time.time()
    while time.time() - start_time < wait_time_seconds:
        try:
            # Check the build status
            response = requests.get(
                f"{job_url}/lastBuild/api/json",
                auth=(username, api_token),
                timeout=10
            )
            response.raise_for_status()
            build_info = response.json()

            if build_info.get('building', False):
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Build #{build_info['number']} is in progress...")
            else:
                result = build_info.get('result')
                build_number = build_info.get('number')
                build_url = build_info.get('url')
                print(f"Build #{build_number} completed with status: {result}")
                print(f"Build URL: {build_url}")

                # Return build information for GHA
                return {
                    "status": result,
                    "build_number": build_number,
                    "build_url": build_url,
                }
        except RequestException as e:
            print(f"Error fetching build status: {e}")
            return {"status": "error", "message": str(e)}

        time.sleep(retry_interval)

    print(f"Job did not complete within the specified wait time ({wait_time_seconds // 10} minutes).")
    return {"status": "timeout", "message": "Job timed out"}
    
# Main entry point 
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python trigger_jenkins_job.py <job_url> <username> <api_token>")

    job_url = sys.argv[1]
    username = sys.argv[2]
    api_token = sys.argv[3]

    result = trigger_jenkins_job(job_url, username, api_token)
    
    # Output result for GitHub Actions
    print(f"status={result['status']}")
    if "build_number" in result and "build_url" in result:
        print(f"build_number={result['build_number']}")
        print(f"build_url={result['build_url']}")

    # Exit with appropriate code
    sys.exit(0 if result['status'] == "SUCCESS" else print(f"status={result['status']}"))
    
              
