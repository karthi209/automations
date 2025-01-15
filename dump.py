import requests
import os
import json
from requests.exceptions import RequestException, ConnectionError, Timeout

def send_request():

    url = "xxx"
    
    # Get token from environment variable
    token = os.getenv('JIRA_API_TOKEN')
    tag = os.getenv('TAG')

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
                "key": os.getenv('JIRA_PROJECT_KEY')
            },
            "summary": f"GHA and Jenkins image versioned v{tag} ready for testing",
            "issuetype":{
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
    
    # Validate payload before sending
    if not isinstance(payload, dict):
        raise ValueError("Invalid payload format")
    
    try:
        with requests.Session() as session:
            response = session.post(
                url,
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()  # Raises an error for bad status codes
            
            # Log success
            print(f"Status Code: {response.status_code}")
            
            # Parse and validate response
            data = response.json()
            return data
            
    except ConnectionError as e:
        print(f"Connection failed: {e}")
    except Timeout as e:
        print(f"Request timed out: {e}")
    except RequestException as e:
        print(f"Request failed: {e}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse response: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None

send_request()
