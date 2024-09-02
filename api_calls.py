import openai
import os
import requests

# Load API key from environment variable

# Define the endpoint for usage
url = "https://api.openai.com/v1/dashboard/billing/usage"

# Make the request
response = requests.get(url, headers={"Authorization": f"Bearer {openai.api_key}"})

# Check the response
if response.status_code == 200:
    usage = response.json()
    print(usage)
else:
    print(f"Error: {response.status_code} - {response.text}")
