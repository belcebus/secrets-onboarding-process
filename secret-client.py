import requests
import json
import base64
import nacl.encoding
import nacl.signing
import nacl.secret
import argparse

# Crea el parser
parser = argparse.ArgumentParser(description="Script para añadir un secreto a un repositorio de GitHub.")

# Agrega los argumentos
parser.add_argument('--name', type=str, required=True, help='Nombre del secreto', metavar='SECRET_NAME')
parser.add_argument('--value', type=str, required=True, help='Valor del secreto', metavar='SECRET_VALUE')
parser.add_argument('--org', type=str, required=True, help='Nombre de la organización o usuario')
parser.add_argument('--repo', type=str, required=True, help='Nombre del repositorio')
parser.add_argument('--token', type=str, required=True, help='Token')
parser.add_argument('--env', type=str, required=False, help='Environment del repositorio al que asociar el secreto')

# Parsea los argumentos
args = parser.parse_args()


secret_name = args.secret_name
secret_value = args.secret_value
owner_name = args.owner_name
repo_name = args.repo_name
token = args.token

# Encriptar el secreto con la clave pública del repositorio usando libsodium

# Obtener la clave pública del repositorio
url = f"https://api.github.com/repos/{owner_name}/{repo_name}/actions/secrets/public-key"
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"Bearer {token}"
}
print("URL: ", url)
print("Headers: ", headers)
# Enviar la petición GET para obtener la clave pública
response = requests.get(url, headers=headers)

public_key = response.json()["key"]
public_key_id = response.json()["key_id"]

print("public_key in BASE64: ", public_key)
print("public_key_id: ", public_key_id)

# Decode the public key from base64
public_key_bytes = base64.b64decode(public_key)

# Encriptar el secreto con la clave pública del repositorio usando libsodium

sealed_box = nacl.public.SealedBox(nacl.public.PublicKey(public_key_bytes))
encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))

print("Encrypted: ", encrypted)

# Añadir el secreto a GitHub

# Definir la URL de la API de GitHub para añadir un secreto
url = f"https://api.github.com/repos/{owner_name}/{repo_name}/actions/secrets/{secret_name}"

# transformar el secreto en base64 en un objeto serializable para poder enviarlo en la peticion
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
print("Headers: ", headers)

# Enviar la petición POST para añadir el secreto
response = requests.put(url, headers=headers, data=json.dumps(data))

print("Response: ", response)   

# Comprobar si la petición ha sido exitosa con un código 201 para un nuevo secreto o
# 204 para la actualización de un secreto existente
if response.status_code == 201:
    print("El secreto ha sido añadido correctamente.")
elif response.status_code == 204:
    print("El secreto ha sido actualizado correctamente.")
else:
    print("Ha ocurrido un error al añadir el secreto.")
