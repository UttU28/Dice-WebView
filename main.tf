variable "terraform-state-rg" {
  type        = string
  description = "RG Name."
}

variable "terraform-state-account" {
  type        = string
  description = "Acoount Name."
}

variable "terraform-state-container" {
  type        = string
  description = "Container Name."
}

variable "terraform-state-webapp" {
  type        = string
  description = "Fiel Name."
}


terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
    }
  }
    backend "azurerm" {
    resource_group_name  = var.terraform-state-rg
    storage_account_name = var.terraform-state-account
    container_name       = var.terraform-state-container
    key                  = var.terraform-state-webapp
  }
}
#   backend "azurerm" {
#     resource_group_name  = local.backend-rg
#     storage_account_name = local.backend-storage
#     container_name       = local.backend-container
#     key                  = local.backend-webapp
#   }
# }


resource "azurerm_resource_group" "example" {
  name = "thisresourcegroup"
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
      docker_image_name        = "thisacr.azurecr.io/dicewebview:latest"
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


