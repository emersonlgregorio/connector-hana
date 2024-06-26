from typing import Any

from spiffworkflow_connector_command.command_interface import ConnectorCommand
from spiffworkflow_connector_command.command_interface import ConnectorProxyResponseDict

from src.connector_hana.base_command import BaseCommand


class DropTable(ConnectorCommand, BaseCommand):

    def __init__(self,
        database_connection_str: str,
        table_name: str
    ):
        """__init__."""
        self.database_connection_str = database_connection_str
        self.table_name = table_name

    def execute(self, _config: Any, _task_data: Any) -> ConnectorProxyResponseDict:

        # TODO: build properly with SQL().format(Identifier(name))
        # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        sql = f"DROP TABLE IF EXISTS {self.table_name};"

        return self.execute_query(sql, self.database_connection_str)

