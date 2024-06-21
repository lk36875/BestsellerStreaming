import os

from azure.identity import DefaultAzureCredential
from azure.schemaregistry import SchemaRegistryClient

__all__ = ["AzureSchemaRegistry"]


class AzureSchemaRegistry:
    """
    Client for interacting with Azure Schema Registry.
    Requires the SCHEMA_REGISTRY_FULLY_QUALIFIED_NAMESPACE environment variable.
    """

    def __init__(
        self,
        credentials=DefaultAzureCredential(),
        fully_qualified_namespace=os.getenv("SCHEMA_REGISTRY_FULLY_QUALIFIED_NAMESPACE"),
    ) -> None:
        """Initialize the AzureSchemaRegistry object.

        Args:
            credentials: Azure credentials.
            fully_qualified_namespace: The fully qualified namespace for the Azure Schema Registry.

        Raises:
            ValueError: If SCHEMA_REGISTRY_FULLY_QUALIFIED_NAMESPACE environment variable is not set.
        """
        self.credentials = credentials
        self.fully_qualified_namespace = fully_qualified_namespace

        if self.fully_qualified_namespace is None:
            raise ValueError("SCHEMA_REGISTRY_FULLY_QUALIFIED_NAMESPACE environment variable not set")

        self.client = SchemaRegistryClient(
            fully_qualified_namespace=self.fully_qualified_namespace, credential=self.credentials
        )

    def get_schema(self, group_name: str, name: str, version: int) -> tuple[str, dict[str, str]]:
        """
        Get the schema definition and properties from the Azure Schema Registry.

        Args:
            group_name: The name of the schema group.
            name: The name of the schema.
            version: The version of the schema.

        Returns:
            The schema definition.
            The schema properties.
        """
        with self.client as schema_registry_client:
            schema = schema_registry_client.get_schema(group_name=group_name, name=name, version=version)
            definition = schema.definition
            properties = schema.properties

        return definition, properties

    def register_schema(self, group_name: str, name: str, schema_definition: str):
        """Register a schema with the Azure Schema Registry.

        Args:
            group_name: The name of the schema group.
            name: The name of the schema.
            schema_definition: The schema definition.

        Returns:
            The schema properties.
        """
        with self.client as schema_registry_client:
            schema_properties = schema_registry_client.register_schema(
                group_name=group_name, name=name, definition=schema_definition, format="Avro"
            )

        return schema_properties


if __name__ == "__main__":
    import logging

    client = AzureSchemaRegistry()
    schema = client.get_schema("base_schema_group", "book_schema", 1)
    logging.info(schema)
