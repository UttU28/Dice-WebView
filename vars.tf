provider "azurerm" {
  features {}
}

# Fetch the existing Key Vault
data "azurerm_key_vault" "example" {
  name                = "thisdicekeyvault"
  resource_group_name = "thisresourcegroup"
}

# Fetch a specific secret from the Key Vault
data "azurerm_key_vault_secret" "example_secret" {
  name      = "username"
  key_vault_id = data.azurerm_key_vault.example.id
}

# Output the secret value
output "example_secret_value" {
  value = data.azurerm_key_vault_secret.example_secret.value
  sensitive = false
}
