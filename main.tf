# provider "azurerm" {
#   features {}
# }

# data "azurerm_resource_group" "example" {
#   name = "thisresourcegroup"
#   #   location = "East US"
# }

# resource "azurerm_service_plan" "example" {
#   name                = "thisismyserviceplan"
#   resource_group_name = data.azurerm_resource_group.example.name
#   location            = "East US"
#   os_type             = "Linux"
#   sku_name            = "B1"
# }

# resource "azurerm_linux_web_app" "example" {
#   name                = "thisismywebapp123321"
#   resource_group_name = data.azurerm_resource_group.example.name
#   location            = azurerm_service_plan.example.location
#   service_plan_id     = azurerm_service_plan.example.id

#   site_config {
#     always_on = true
#     application_stack {
#       docker_image_name        = "thisacr.azurecr.io/imagename:latest"
#       docker_registry_username = "thisacr"
#       docker_registry_password = "U9+ivfherZPq3+UWDnj1fxftpOqWUgXqspIc90YYFI+ACRBkerUy"
#     }
#   }

# }

# resource "null_resource" "restart_web_app" {
#   depends_on = [azurerm_linux_web_app.example]

#   provisioner "local-exec" {
#     command = <<EOT
#     az webapp restart --resource-group ${data.azurerm_resource_group.example.name} --name ${azurerm_linux_web_app.example.name}
#     EOT
#   }
# }


