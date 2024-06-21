resource "azurerm_eventhub_namespace" "eh_namespace" {
  auto_inflate_enabled     = false
  capacity                 = 1
  location                 = azurerm_resource_group.kafka_rg.location
  maximum_throughput_units = 0
  name                     = "kafka-namespace"
  network_rulesets = [
    {
      public_network_access_enabled  = true
      default_action                 = "Allow"
      ip_rule                        = []
      trusted_service_access_enabled = false
      virtual_network_rule           = []
    },
  ]
  resource_group_name = azurerm_resource_group.kafka_rg.name
  sku                 = "Standard"

  zone_redundant = true

  timeouts {}
}

resource "azurerm_eventhub" "books_eh" {
  name                = "books"
  namespace_name      = azurerm_eventhub_namespace.eh_namespace.name
  resource_group_name = azurerm_eventhub_namespace.eh_namespace.resource_group_name
  partition_count     = 2
  message_retention   = 7
}


resource "azurerm_eventhub_namespace_schema_group" "eh_schema_group" {
  name                 = "base_schema_group"
  namespace_id         = azurerm_eventhub_namespace.eh_namespace.id
  schema_compatibility = "Forward"
  schema_type          = "Avro"
}

