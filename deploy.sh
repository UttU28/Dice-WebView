RESOURCE_ID=$(az group show --resource-group dicetestapply_group --query id --output tsv)
/subscriptions/e4cf2944-5342-4787-b990-418828e5555539bfc/resourceGroups/dicetestapply_group
echo $RESOURCE_ID



az appservice plan create --name thatappserviceplan --resource-group dicetestapply_group --sku B1 --is-linux



az webapp create --resource-group $RESOURCE_GROUP_NAME --plan $appServicePlanName --name $webAppName --assign-identity '[system]' --scope /subscriptions/$subscriptionID/resourceGroups/$RESOURCE_GROUP_NAME --role acrpull --runtime "PYTHON|3.9" --deployment-container-image-name thisacr.azurecr.io/imagename:latest
az webapp config set --resource-group $RESOURCE_GROUP_NAME --name $webAppName --generic-configurations '{"acrUseManagedIdentityCreds": true}'



CREDENTIAL=$(az webapp deployment list-publishing-credentials --resource-group dicetestapply_group --name dicesaralapply --query publishingPassword --output tsv)
echo $CREDENTIAL


# SERVICE_URI='https://$dicesaralapply:'$CREDENTIAL'@dicesaralapply.scm.azurewebsites.net/api/registry/webhook'

# az acr webhook create --name webhookforwebapp --registry thisacr --scope msdocspythoncontainerwebapp:* --uri $SERVICE_URI --actions push




------------

RESOURCE_GROUP_NAME='dicetestapply_group'
RESOURCE_ID=$(az group show --resource-group $RESOURCE_GROUP_NAME --query id --output tsv)
echo $RESOURCE_ID


RESOURCE_GROUP_NAME='thisresourcegroup'
APP_SERVICE_PLAN_NAME='thatappserviceplan'
az appservice plan create --name thatappserviceplan --resource-group thisresourcegroup --sku B1 --is-linux

APP_SERVICE_NAME='dicesaralapply'
REGISTRY_NAME='thisacr'
CONTAINER_NAME=$REGISTRY_NAME'.azurecr.io/imagename:latest'
az webapp create --resource-group $RESOURCE_GROUP_NAME --plan $APP_SERVICE_PLAN_NAME --name $APP_SERVICE_NAME --assign-identity '[system]' --scope $RESOURCE_ID --role acrpull --deployment-container-image-name $CONTAINER_NAME


