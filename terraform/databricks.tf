resource "azurerm_databricks_workspace" "databricks" {
  name                        = "kafka-processing-databricks"
  location                    = azurerm_resource_group.kafka_rg.location
  resource_group_name         = azurerm_resource_group.kafka_rg.name
  sku                         = "trial"
  managed_resource_group_name = "managed-kafka-processing-databricks-rg"

}

data "azurerm_subscription" "primary" {}

data "azuread_application_published_app_ids" "well_known" {}


resource "azurerm_key_vault" "kv_databricks" {
  name                       = var.key_vault_name
  location                   = azurerm_resource_group.kafka_rg.location
  resource_group_name        = azurerm_resource_group.kafka_rg.name
  tenant_id                  = data.azurerm_subscription.primary.tenant_id
  soft_delete_retention_days = 7
  purge_protection_enabled   = false
  sku_name                   = "standard"
  enable_rbac_authorization  = true
}

data "azuread_service_principal" "databricks_sp" {
  display_name = "AzureDatabricks"
}

resource "azurerm_role_assignment" "rbac_databricks_kv" {
  scope                = azurerm_resource_group.kafka_rg.id
  role_definition_name = "Key Vault Administrator"
  principal_id         = data.azuread_service_principal.databricks_sp.id
}

# Schema contributor is also needed for both managed identities of databricks

output "key_vault_data" {
  value = [azurerm_key_vault.kv_databricks.vault_uri, azurerm_key_vault.kv_databricks.id]
}