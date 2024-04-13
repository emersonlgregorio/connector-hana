
from typing import Any

from spiffworkflow_connector_command.command_interface import ConnectorCommand
from spiffworkflow_connector_command.command_interface import ConnectorProxyResponseDict

from src.connector_hana.base_command import BaseCommand


class SelectValues(BaseCommand, ConnectorCommand):

    def __init__(self,
        database_connection_str: str,
        table_name: str,
        schema: dict[str, Any]
    ):
        """__init__."""
        self.database_connection_str = database_connection_str
        self.table_name = table_name
        self.schema = schema

    def execute(self):#, _config: Any, _task_data: Any) -> ConnectorProxyResponseDict:

        columns = ",".join(self.schema["columns"])
        where_clause, values = self.build_where_clause(self.schema)

        # TODO: build properly with SQL().format(Identifier(name))
        # https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        sql = f"SELECT {columns} FROM {self.table_name} {where_clause};"  # noqa: S608

        return self.fetchall(sql, self.database_connection_str, values)


if __name__ == '__main__':
   connHana = {"address": "172.20.1.4",
               "port": "30015",
               "user": "SYSTEM",
               "password": "9Ab63^Op33"
               }
   table =  "SBO_CRESTANI_QA.\"Entidade\""
   schema = {
       "columns": [
           "\"ID\"",
           "\"NomeFantasia\"",
           "\"CNPJ\""
       ]
   }
   teste = SelectValues(connHana,table,schema)
   result = teste.execute()
   print(result)