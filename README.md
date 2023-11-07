# secrets-onboarding-process
Python script to add secrets to a repository.

## Requisitos

Se requiere un token de grano fino con permisos de lectura y escritura en los secretos del repositorio.

## Uso del script

### Creación del entorno virtual
```bash
python -m venv venv
```

### instalación de dependencias

```bash
pip install -r requirements.txt
```

### Ejecución del script

```bash
usage: secret-client.py [-h] --name SECRET_NAME --value SECRET_VALUE --org ORG --repo REPO --token TOKEN [--env ENV]

Script para añadir un secreto a un repositorio de GitHub.

options:
  -h, --help            show this help message and exit
  --name SECRET_NAME    Nombre del secreto
  --value SECRET_VALUE  Valor del secreto
  --org ORG             Nombre de la organización o usuario
  --repo REPO           Nombre del repositorio
  --token TOKEN         Token
  --env ENV             Environment del repositorio al que asociar el secreto
```

Example to create a new secret in a repository:

```bash
python secret-client.py --name SECRET_NAME --value SECRET_VALUE --org ORG --repo REPO --token TOKEN 
```

Example to create a new secret in a repository and associate it with an environment:

```bash
python secret-client.py --name SECRET_NAME --value SECRET_VALUE --org ORG --repo REPO --token TOKEN --env ENV
```