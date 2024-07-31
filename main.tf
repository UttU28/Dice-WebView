terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
    }
  }
  backend "azurerm" {
    resource_group_name  = local.secret_values["backend-rg"]
    storage_account_name = local.secret_values["backend-storage"]
    container_name       = local.secret_values["backend-container"]
    key                  = local.secret_values["backend-webapp"]
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name = "thisresourcegroup"
  location = local.secret_values["general-location"]
}

resource "azurerm_service_plan" "example" {
  name                = local.secret_values["webapp-service-plan"]
  resource_group_name = data.azurerm_resource_group.example.name
  location            = local.secret_values["general-location"]
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "example" {
  name                = local.secret_values["webapp-name"]
  resource_group_name = data.azurerm_resource_group.example.name
  location            = azurerm_service_plan.example.location
  service_plan_id     = azurerm_service_plan.example.id

  site_config {
    always_on = true
    application_stack {
      docker_image_name        = "thisacr.azurecr.io/dicewebview:latest"
      docker_registry_username = local.secret_values["acrName"]
      docker_registry_password = local.secret_values["acrPassword"]
    }
  }

}

resource "null_resource" "restart_web_app" {
  depends_on = [azurerm_linux_web_app.example]

  provisioner "local-exec" {
    command = <<EOT
    sleep 60

    az webapp restart --resource-group ${data.azurerm_resource_group.example.name} --name ${azurerm_linux_web_app.example.name}
    EOT
  }
}


