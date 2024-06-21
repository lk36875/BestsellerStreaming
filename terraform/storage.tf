
resource "azurerm_storage_account" "kafka_storage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.kafka_rg.name
  location                 = azurerm_resource_group.kafka_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = true
  access_tier              = "Hot"

}

resource "azurerm_storage_container" "books_container" {
  name                  = "books-container"
  storage_account_name  = azurerm_storage_account.kafka_storage.name
  container_access_type = "private"
}
