terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
    }
  }
  backend "azurerm" {
    resource_group_name  = "thisstoragerg"
    storage_account_name = "dicestorage02"
    container_name       = "13form"
    key                  = "webappState"
  }
}


data "azurerm_resource_group" "resource_group" {
  name     = local.jobscraping-rg
}

data "azurerm_log_analytics_workspace" "analytics_workspace" {
  name                = local.jobscraping-log-analytics-workspace
  resource_group_name = data.azurerm_resource_group.resource_group.name
}

data "azurerm_container_app_environment" "app_environment" {
  name                = local.jobscraping-app-environment
  location            = local.general-location
  resource_group_name = data.azurerm_resource_group.resource_group.name
}

resource "azurerm_container_app" "dicesaralapply11" {
  name                         = "dicesaralapply11-app"
  container_app_environment_id = data.azurerm_container_app_environment.app_environment.id
  resource_group_name          = data.azurerm_resource_group.resource_group.name
  revision_mode                = "Single"

  template {
    container {
      name   = "${local.acrName}-random-string"
      image  = local.acrUrl
      cpu    = 0.75
      memory = "1.5Gi"

      env {
        name  = "databaseServer"
        value = local.databaseServer
      }
      env {
        name  = "databaseName"
        value = local.databaseName
      }
      env {
        name  = "databaseUsername"
        value = local.databaseUsername
      }
      env {
        name  = "databasePassword"
        value = local.databasePassword
      }
      env {
        name  = "blobConnectionString"
        value = local.blobConnectionString
      }
      env {
        name  = "resumeContainer"
        value = local.resumeContainer
      }
    }
  }

  secret {
    name  = "registry-credentials"
    value = local.acrPassword
  }
  registry {
    server               = "${local.acrName}.azurecr.io"
    username             = local.acrName
    password_secret_name = "registry-credentials"
  }
}