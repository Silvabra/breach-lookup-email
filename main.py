#!/usr/bin/env python3

import requests
import sys
import time
import json

API_KEY = "bc8c4467b1ae6ee6b8db909d4806b18a1f1c2073c96b1749fc1ad870c90956fe"
BASE_URL = "https://api.databreach.zip"

def create_job(email):
    url = f"{BASE_URL}/api/create_job.php"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {"q": email, "limit": 100}
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    if "error" in result:
        print(f"Error creating job: {result['error']}")
        sys.exit(1)
    
    return result.get("job_id")

def check_status(job_id):
    url = f"{BASE_URL}/api/job_status.php?id={job_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    response = requests.get(url, headers=headers)
    return response.json()

def fetch_results(job_id):
    url = f"{BASE_URL}/api/job_fetch.php?id={job_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    response = requests.get(url, headers=headers)
    return response.json()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <email>")
        sys.exit(1)
    
    email = sys.argv[1]
    print(f"Searching for: {email}")
    
    print("Creating job...")
    job_id = create_job(email)
    print(f"Job ID: {job_id}")
    
    print("Waiting for job to complete...")
    while True:
        status_response = check_status(job_id)
        status = status_response.get("job", {}).get("status", "")
        
        if status == "success":
            print("Job completed!")
            break
        elif status == "failed":
            print("Job failed")
            sys.exit(1)
        elif status == "pending":
            print(".", end="", flush=True)
            time.sleep(3)
        else:
            print(f"Unknown status: {status}")
            sys.exit(1)
    
    print()
    
    print("Fetching results...")
    results = fetch_results(job_id)
    
    if results.get("status") == "success":
        data = results.get("response", [])
        print(f"\nFound {len(data)} results:\n")
        print(json.dumps(data, indent=2))
    else:
        print("No results found or error occurred")

if __name__ == "__main__":
    main()
