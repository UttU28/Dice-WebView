# from azure.identity import DefaultAzureCredential
# from azure.keyvault.secrets import SecretClient
import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# Replace with your Azure Key Vault name
# KEY_VAULT_NAME = "thisdicekeyvault"
# KV_URI = f"https://{KEY_VAULT_NAME}.vault.azure.net"

# def getSecrets(nameList):
#     """
#     Retrieve secrets from Azure Key Vault and set them as environment variables.
    
#     Args:
#         nameList (list): List of secret names to retrieve.
#     """
#     credential = DefaultAzureCredential()
#     client = SecretClient(vault_url=KV_URI, credential=credential)
    
#     # Retrieve and set secrets as environment variables
#     for secret_name in nameList:
#         try:
#             secret = client.get_secret(secret_name)
#             os.environ[secret_name] = secret.value
#             print(f"Secret '{secret_name}' has been set as an environment variable.")
#         except Exception as e:
#             print(f"An error occurred while retrieving '{secret_name}': {e}")

#     # Close the client
#     client.close()

# # Define the list of secrets you want to retrieve
# secrets_list = [
#     'databaseServer',
#     'databaseName',
#     'databaseUsername',
#     'databasePassword',
#     'blobConnectionString',
#     'resumeContainer'
# ]

# # Retrieve secrets and set environment variables
# getSecrets(secrets_list)

# Ensure environment variables are set before configuring classes

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')  # For session management, CSRF protection, etc.

class AzureSQLConfig(Config):
    # databaseServer = os.getenv('databaseServer')
    print(os.getenv('databaseServer'), "os.getenv('databaseServer')os.getenv('databaseServer')")
    # databaseName = os.getenv('databaseName')
    # databaseUsername = os.getenv('databaseUsername')
    # databasePassword = os.getenv('databasePassword')
    databaseServer='dice-sql.database.windows.net'
    databaseName='dice_sql_database'
    databaseUsername='iAmRoot'
    databasePassword='Qwerty@213'
    connectionString = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server=tcp:{databaseServer},1433;"
        f"Database={databaseName};"
        f"Uid={databaseUsername};"
        f"Pwd={databasePassword};"
        f"Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )

class AzureBLOBConfig(Config):
    AZURE_CONNECTION_STRING='DefaultEndpointsProtocol=https;AccountName=dicestorage02;AccountKey=OFusrDHbeLjeipF0m836T13AakwgBzaX7gbAl+Cjw46N1K/dEEHvVbiC2Mw+JYE67v+2KNqg7BAN+AStPE7SGw==;EndpointSuffix=core.windows.net'
    CONTAINER_NAME='resume-data'
    # AZURE_CONNECTION_STRING = os.getenv('blobConnectionString')
    # CONTAINER_NAME = os.getenv('resumeContainer')

# databaseServer = 'dice-sql.database.windows.net'
# databaseName = 'dice_sql_database'
# databaseUsername = 'iAmRoot'
# databasePassword = 'Qwerty@213'
# connectionString = f'Driver={{ODBC Driver 17 for SQL Server}};Server=tcp:{databaseServer},1433;Database={databaseName};Uid={databaseUsername};Pwd={databasePassword};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
