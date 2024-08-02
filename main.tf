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

resource "azurerm_resource_group" "example" {
  name     = local.webapp-rg
  location = local.general-location
}

resource "azurerm_service_plan" "example" {
  name                = local.webapp-service-plan
  resource_group_name = azurerm_resource_group.example.name
  location            = local.general-location
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "example" {
  name                = local.webapp-name
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_service_plan.example.location
  service_plan_id     = azurerm_service_plan.example.id

  site_config {
    always_on = true
    application_stack {
      docker_image_name        = local.acrUrl
      docker_registry_username = local.acrName
      docker_registry_password = local.acrPassword
    }
  }

}

resource "null_resource" "restart_web_app" {
  depends_on = [azurerm_linux_web_app.example]

  provisioner "local-exec" {
    command = <<EOT
    sleep 60

    az webapp restart --resource-group ${azurerm_resource_group.example.name} --name ${azurerm_linux_web_app.example.name}
    EOT
  }
}


