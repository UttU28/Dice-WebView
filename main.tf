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

data "azurerm_container_app_environment" "app_environment" {
  name                = "this-dice-jobscraping-app-environment"
  resource_group_name = "this-dice-jobscraping-rg"
}

resource "azurerm_container_app" "dicesaralapply11" {
  name                         = "dicesaralapply11-app"
  container_app_environment_id = data.azurerm_container_app_environment.app_environment.id
  resource_group_name          = "this-dice-jobscraping-rg"
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

  provisioner "local-exec" {
    command = <<EOT
      az containerapp ingress enable \
        --name ${self.name} \
        --resource-group ${self.resource_group_name} \
        --type external \
        --target-port 50505 \
        --transport auto \
        --allow-insecure false
    EOT
  }
}
