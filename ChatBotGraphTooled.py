from SuperVisorv2 import decide_and_execute
from ChatBotHelper.SQLSupervisor import SQLdecide_and_execute
from ChatBotHelper.GeneralResponse import genericResponse
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END


class ChatbotState(TypedDict):
    user_input: str
    messages: list  # LangGraph expects 'messages' as the key for state updates
    query_type: str # This will store 'sql_generation' or 'general_response'

def build_chatbot_graph(llm, schema_context, sql_prompt_template, memory, supabase):
    workflow = StateGraph(ChatbotState)

    tools = {
        "decide_and_execute":lambda state: decide_and_execute(state, llm, schema_context, sql_prompt_template, memory, supabase, formatType = "json")
        ,"genericResponse":lambda state: genericResponse(state, llm, memory)
        ,"SQLSupervisor":lambda state: SQLdecide_and_execute(state, llm, schema_context, sql_prompt_template,  memory,supabase, formatType = "json")
    }

    # Add workflow nodes
    workflow.add_node("decide_and_execute", tools["decide_and_execute"])
    workflow.add_node("genericResponse", tools["genericResponse"])
    workflow.add_node("SQLSupervisor", tools["SQLSupervisor"])
    #workflow.add_node("SQLAgent", tools["SQLAgent"])

    # Conditional Routing based on Decision Agent
    #workflow.add_conditional_edges("decide_and_execute", lambda state: "genericResponse" if state["query_type"] == "general_response" else "SQLAgent")
    # Conditional routing with logs
    def route_based_on_query_type(state):
        #print(f"Routing decision: query_type={state['query_type']}")
        return "SQLSupervisor" if state["query_type"] == "domain_specific" else "genericResponse"

    #workflow.add_conditional_edges("decide_and_execute", lambda state: "SQLSupervisor" if state["query_type"] == "domain_specific" else "genericResponse")
    workflow.add_conditional_edges("decide_and_execute", route_based_on_query_type)

    # Set entry point
    workflow.set_entry_point("decide_and_execute")
    workflow.add_edge("decide_and_execute", END)

    return workflow.compile()