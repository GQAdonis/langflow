from typing import Callable, Union

from langchain.agents import AgentExecutor
from langchain.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent

from langflow.field_typing import BaseLanguageModel
from langflow.interface.custom.custom_component import CustomComponent


class SQLAgentComponent(CustomComponent):
    display_name = "SQLAgent"
    description = "Construct an SQL agent from an LLM and tools."

    def build_config(self):
        return {
            "llm": {"display_name": "LLM"},
            "database_uri": {"display_name": "Database URI"},
            "verbose": {"display_name": "Verbose", "value": False, "advanced": True},
        }

    def build(
        self,
        llm: BaseLanguageModel,
        database_uri: str,
        verbose: bool = False,
    ) -> Union[AgentExecutor, Callable]:
        schema = os.getenv("LANGFLOW_DATABASE_SCHEMA")
        if schema is None:
            schema = "public"
        db = SQLDatabase.from_uri(database_uri, schema=schema)
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        return create_sql_agent(llm=llm, toolkit=toolkit)
