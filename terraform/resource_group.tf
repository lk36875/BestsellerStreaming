resource "azurerm_resource_group" "kafka_rg" {
  name     = "kafka-processing-rg"
  location = var.region
  tags = {
    "CreatedBy" = "terraform"
  }
}
