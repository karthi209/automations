import requests
import os
import json
from requests.exceptions import RequestException, ConnectionError, Timeout

def send_request():
    url = "xxx"
    
    token = os.getenv('JIRA_API_TOKEN')
    tag = os.getenv('TAG')
    project_key = os.getenv('JIRA_PROJECT_KEY')

    # Debug environment variables (without exposing token)
    print(f"Tag value: {tag}")
    print(f"Project key: {project_key}")
    print(f"Token present: {'Yes' if token else 'No'}")
    
    if not token:
        raise ValueError("API token not found in environment variables")
        
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    payload = {
        "fields": {
            "project": {
                "key": project_key
            },
            "summary": f"GHA and Jenkins image versioned v{tag} ready for testing",
            "issuetype": {
                "name": "Task"
            },
            "description": f"""New image is now in staging and ready to be tested.
            Please use the label "staging" to test images.
            
            Refer below links for testing results and pre-release notes.
            
            Pre-release notes for image version v{tag}
            https://github.xxx.com/devsecops/agent_build/releases/tag/{tag}.jenkins.bluemix.all.tools
            
            Unit testing results
            https://github.xxx.com/devsecops/agent_build/wiki/unit_test_results_v{tag}
            
            Integration testing results (User provided jobs) 
            https://github.xxx.com/devsecops/agent_build/wiki/integration_test_results_v{tag}
            
            Molecule testing results
            https://github.xxx.com/devsecops/agent_build/wiki/molecule_test_results_v{tag}
            
            Please comment in this ticket for feedback."""
        }
    }
    
    try:
        print("\nSending request with:")
        print(f"URL: {url}")
        print("Headers:", {k: v if k != 'Authorization' else '[REDACTED]' for k, v in headers.items()})
        print("Payload:", json.dumps(payload, indent=2))
        
        with requests.Session() as session:
            response = session.post(
                url,
                headers=headers,
                json=payload
            )
            
            print(f"\nResponse Status Code: {response.status_code}")
            print("Response Headers:", dict(response.headers))
            print("Response Body:", response.text)
            
            if response.status_code == 400:
                try:
                    error_details = response.json()
                    print("\nDetailed error information:", json.dumps(error_details, indent=2))
                except:
                    print("Could not parse error response as JSON")
            
            response.raise_for_status()
            
            data = response.json()
            return data
            
    except ConnectionError as e:
        print(f"Connection failed: {e}")
    except Timeout as e:
        print(f"Request timed out: {e}")
    except RequestException as e:
        print(f"Request failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Error response: {e.response.text}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse response: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None

if __name__ == "__main__":
    result = send_request()
