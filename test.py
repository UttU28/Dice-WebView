import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

KVUri = f"https://thisdicekeyvault.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

allSecrets = {
    # "backend-rg": "thisstoragerg",
    # "backend-storage": "dicestorage02",
    # "backend-container": "13form",
    # "backend-webapp": "webappState",
    # "general-location": "East US",
    # "backend-datascraping": "datascrapingState",
    # "webapp-rg": "this-dice-webapp-rg",
    # "webapp-service-plan": "this-dice-webapp-service-plan",
    # "webapp-name": "dicesaralapply",
    # "webapp-image": "dicewebview",
    # "acrName": "thisacr",
    # "acrPassword": "U9+ivfherZPq3+UWDnj1fxftpOqWUgXqspIc90YYFI+ACRBkerUy"
    # "webapp": "sdv",
    # "sdv": "sdv",
    # "sdv": "sdv",
    # "sdv": "sdv",
    # "sdv": "sdv",
    # "sdv": "sdv",
}

for secretsKey, secretsValue in allSecrets.items():
    print(secretsKey, secretsValue)
    client.set_secret(str(secretsKey), str(secretsValue))


print(" done.")