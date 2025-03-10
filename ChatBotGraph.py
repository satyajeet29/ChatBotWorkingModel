from typing import TypedDict
from langgraph.graph import StateGraph
from Supervisor import decide_and_execute  # Import your state type
from langchain.schema import SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Define State Type
class ChatbotState(TypedDict):
    user_input: str
    messages: list  # LangGraph expects 'messages' as the key for state updates

def build_chatbot_graph(llm, schema_context, sql_prompt_template, memory, supabase):
    """Defines and compiles the chatbot graph."""

    def decision_agent(state):
        return decide_and_execute(state, llm, schema_context, sql_prompt_template, memory, supabase)

    workflow = StateGraph(ChatbotState)
    workflow.add_node("decision_agent", decision_agent)
    workflow.set_entry_point("decision_agent")
    workflow.add_edge("decision_agent", END)

    return workflow.compile()  # Return compiled app
