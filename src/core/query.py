import src.constant as constant

from langchain_astradb import AstraDBVectorStore
from langchain_milvus import Milvus
from typing import Union, Dict, List
from src.services.logger_service import LoggerService
from src.services.memory_factory import MemoryFactory
from src.services.llm_factory import ChatCohere, ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor, create_tool_calling_agent

logger = LoggerService.get_logger(__name__)


class Query:
    def __init__(self, vectorstore: Union[AstraDBVectorStore, Milvus]):
        self.vectorstore = vectorstore
        self.retriever = None
        self.memory = None

    def __initialize_query_pipeline(
        self,
        filter: Dict[str, str] = None,
        top_k: int = 4,
        session_id: str = None,
        memory_service: str = None,
    ):
        try:
            self.retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={
                    "k": top_k,
                    "filter": filter,
                },
            )
            self.memory = MemoryFactory.get_memory_instance(
                memory_service=memory_service,
                session_id=session_id,
            )
            tools = [
                create_retriever_tool(
                    retriever=self.retriever,
                    name="Retrieval_QA",
                    description="Retrieves relevant documents from the vector store.",
                )
            ]
            return tools
        except Exception as e:
            logger.error(f"Error initializing query pipeline: {e}")

    def __get_message_history(self):
        messages = self.memory.messages[-4:] if self.memory.messages else []
        return messages

    def __add_message_history(
        self,
        query: str,
        response: str,
    ) -> None:
        self.memory.add_user_message(query)
        self.memory.add_ai_message(response)

    def generate_response(
        self,
        query: str,
        category: str = None,
        sub_category: str = None,
        source: str = None,
        top_k: int = 4,
        session_id: str = None,
        memory_service: str = None,
        llm: Union[ChatCohere, ChatGoogleGenerativeAI] = None,
    ):
        try:
            filter = {
                "category": category,
                "sub_category": sub_category,
                "source": source,
            }
            clean_filter = {k: v for k, v in filter.items() if v}
            tools = self.__initialize_query_pipeline(
                filter=clean_filter,
                top_k=top_k,
                session_id=session_id,
                memory_service=memory_service,
            )
            history_messages = self.__get_message_history()
            PROMPT = ChatPromptTemplate.from_messages(
                [
                    SystemMessage(content=constant.SYSTEM_PROMPT),
                    *history_messages,
                    HumanMessage(content=query),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]
            )
            agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=PROMPT)
            agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=False,
                handle_parsing_errors=True,
                return_intermediate_steps=True,
            )
            response = agent_executor.invoke(
                input={
                    "input": query,
                },
                return_only_outputs=True,
            )
            self.__add_message_history(query=query, response=response["output"])
            return response
        except Exception as e:
            logger.error(f"Error in response generation: {e}")
