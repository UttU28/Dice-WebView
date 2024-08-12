provider "azurerm" {
  features {}
}

# Fetch the existing Key Vault
data "azurerm_key_vault" "thiskeyvault" {
  name                = "thisdicekeyvault"
  resource_group_name = "thisresourcegroup"
}

# Fetch secrets from the Key Vault
data "azurerm_key_vault_secret" "backend-rg" {
  name         = "backend-rg"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "backend-storage" {
  name         = "backend-storage"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "webapp-service-plan" {
  name         = "webapp-service-plan"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "backend-container" {
  name         = "backend-container"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "backend-webapp" {
  name         = "backend-webapp"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "general-location" {
  name         = "general-location"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "backend-datascraping" {
  name         = "backend-datascraping"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "webapp-rg" {
  name         = "webapp-rg"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "webapp-name" {
  name         = "webapp-name"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "webapp-image" {
  name         = "webapp-image"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "acrName" {
  name         = "acrName"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "acrPassword" {
  name         = "acrPassword"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "jobscraping-rg" {
  name         = "jobscraping-rg"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "jobscraping-log-analytics-workspace" {
  name         = "jobscraping-log-analytics-workspace"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

data "azurerm_key_vault_secret" "jobscraping-app-environment" {
  name         = "jobscraping-app-environment"
  key_vault_id = data.azurerm_key_vault.thiskeyvault.id
}

# Define local variables to store the secret values
locals {
  backend-rg           = data.azurerm_key_vault_secret.backend-rg.value
  backend-storage      = data.azurerm_key_vault_secret.backend-storage.value
  webapp-service-plan  = data.azurerm_key_vault_secret.webapp-service-plan.value
  backend-container    = data.azurerm_key_vault_secret.backend-container.value
  backend-webapp       = data.azurerm_key_vault_secret.backend-webapp.value
  general-location     = data.azurerm_key_vault_secret.general-location.value
  backend-datascraping = data.azurerm_key_vault_secret.backend-datascraping.value
  webapp-rg            = data.azurerm_key_vault_secret.webapp-rg.value
  webapp-name          = data.azurerm_key_vault_secret.webapp-name.value
  webapp-image         = data.azurerm_key_vault_secret.webapp-image.value
  acrName              = data.azurerm_key_vault_secret.acrName.value
  acrPassword          = data.azurerm_key_vault_secret.acrPassword.value
  acrUrl               = "${local.acrName}.azurecr.io/${local.webapp-image}:latest"
  jobscraping-rg                      = data.azurerm_key_vault_secret.jobscraping-rg.value
  jobscraping-log-analytics-workspace = data.azurerm_key_vault_secret.jobscraping-log-analytics-workspace.value
  jobscraping-app-environment         = data.azurerm_key_vault_secret.jobscraping-app-environment.value
}

