provider "azurerm" {
  features {}
}

# Fetch the existing Key Vault
data "azurerm_key_vault" "thiskeyvault" {
  name                = "thisdicekeyvault"
  resource_group_name = "thisresourcegroup"
}

# List of secrets to fetch
locals {
  secret_names = [
    "backend-rg",
    "backend-storage",
    "backend-container",
    "backend-webapp",
    "general-location",
    "backend-datascraping",
    "webapp-rg",
    "webapp-service-plan",
    "webapp-name",
    "webapp-image",
    "acrName",
    "acrPassword"
  ]
}

# Fetch all secrets using a loop
data "azurerm_key_vault_secret" "all_secrets" {
  for_each    = toset(local.secret_names)
  name        = each.key
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

# Set local values for all secrets
locals {
  secret_values = { for s in local.secret_names : s => data.azurerm_key_vault_secret.all_secrets[s].value }
}

# You can now access each secret value with local.secret_values["<secret_name>"]
