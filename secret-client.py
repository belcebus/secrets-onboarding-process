import requests
import json
import base64
import nacl.encoding
import nacl.signing
import nacl.secret
import argparse

# Create the parser
parser = argparse.ArgumentParser(description="Script to add a secret to a GitHub repository.")

# Add the arguments
parser.add_argument('--name', type=str, required=True, help='Name of the secret', metavar='SECRET_NAME')
parser.add_argument('--value', type=str, required=True, help='Value of the secret', metavar='SECRET_VALUE')
parser.add_argument('--org', type=str, required=True, help='Name of the organization or user')
parser.add_argument('--repo', type=str, required=True, help='Name of the repository')
parser.add_argument('--token', type=str, required=True, help='Token')
parser.add_argument('--env', type=str, required=False, help='Repository environment to associate the secret with')

# Parse the arguments
args = parser.parse_args()


secret_name = args.name
secret_value = args.value
owner_name = args.org
repo_name = args.repo
token = args.token
environment = args.env

# Encrypt the secret with the repository's public key using libsodium

# Get the repository's public key
url = f"https://api.github.com/repos/{owner_name}/{repo_name}/actions/secrets/public-key"
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"Bearer {token}"
}
print("URL: ", url)
print("Headers: ", headers)
# Send the GET request to get the public key
response = requests.get(url, headers=headers)

public_key = response.json()["key"]
public_key_id = response.json()["key_id"]

print("public_key in BASE64: ", public_key)
print("public_key_id: ", public_key_id)

# Decode the public key from base64
public_key_bytes = base64.b64decode(public_key)

# Encrypt the secret with the repository's public key using libsodium

sealed_box = nacl.public.SealedBox(nacl.public.PublicKey(public_key_bytes))
encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))

print("Encrypted: ", encrypted)

# Add the secret to GitHub

url = ""

# Define the GitHub API URL to add a secret
if environment:
    # Define the GitHub API URL to add a secret with an environment
    url = f"https://api.github.com/repos/{owner_name}/{repo_name}/environments/{environment}/secrets/{secret_name}"
else:
    url = f"https://api.github.com/repos/{owner_name}/{repo_name}/actions/secrets/{secret_name}"

# Transform the base64-encoded secret into a serializable object to be able to send it in the request
encrypted_value = base64.b64encode(encrypted).decode("utf-8")
data = {
    "encrypted_value": encrypted_value,
    "key_id": public_key_id
}
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}

print("URL: ", url)
print("Data: ", data)

# Send the PUT request to add the secret
response = requests.put(url, headers=headers, data=json.dumps(data))

print("Response: ", response)   

# Check if the request was successful with a 201 code for a new secret or
# 204 for an existing secret update
if response.status_code == 201:
    print("The secret has been added successfully.")
elif response.status_code == 204:
    print("The secret has been updated successfully.")
else:
    print("An error occurred while adding the secret.")
