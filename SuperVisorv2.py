from ChatBotHelper.generateSQLQuery import generate_sql_query
from ChatBotHelper.SQLAgent import SQLAgent
from langchain.schema import SystemMessage


def decide_and_execute(state, llm, schemaContext, sqlPromptTemplate, memory,supabase,formatType = "json"):

    user_input = state["user_input"]

    # LLM decides the type of query
    system_message = SystemMessage(
        #content="Classify if the query requires SQL execution ('sql_generation') or is a general response ('general_response'). Only return 'sql_generation' or 'general_response'.")
        content="""Classify the user query into one of the following categories: 
                    - 'domain_specific' if the query is related to topics such as users, property access, energy consumption, anomalies, weather, property data, benchmarking, or utilities
                    - 'general_response' if the query is unrelated to these topics.

                    Examples:
                    - "What is the weather forecast for tomorrow?" → 'domain_specific'
                    - "How much energy did Building X consume last month?" → 'domain_specific'
                    - "What properties do I have access to?" → 'domain_specific'
                    - "Can I make changes to Property X?" → 'domain_specific'
                    - "Why can’t I see Property Y?" → 'domain_specific'
                    - "What is the energy consumption for Property X this month?" → 'domain_specific'
                    - "Which system of property Y is taking more energy?" → 'domain_specific'
                    - "How was my energy consumption for Month A this year compared to Month A last year?" → 'domain_specific'
                    - "Which facade of Property X needs immediate attention?" → 'domain_specific'
                    - "What are the critical points that I need to address?" → 'domain_specific'
                    - "What anomalies have been found for property A?" → 'domain_specific'
                    - "Where can I upload documents for Property X?" → 'domain_specific'
                    - "How many floors are there in building X?" → 'domain_specific'
                    - "Where does my building stand in comparison to other buildings of the same size?" → 'domain_specific'
                    - "Has my Energy Star score improved over time?" → 'domain_specific'
                    - "What is the payback period for [X energy conservation measure] ?" → 'domain_specific'
                    - "What is the forecasted weather for Property X?" → 'domain_specific'
                    - "What was the average monthly weather data for Property Y?" → 'domain_specific'  
                    - "Hi, how are you?" → 'general_response'
                    - "Tell me a joke." → 'general_response'
    
    Only return 'domain_specific' or 'general_response'.""")
    decision = llm.invoke([system_message, user_input]).content.strip()
    memory.save_context({"input": user_input}, {"output": decision})
    #return decision
    #print(f"Decision made by decide_and_execute: {decision}")
    #return {"query_type": decision if decision in ["domain_specific", "general_response"] else "general_response"}

    state["query_type"] = decision if decision in {"domain_specific", "general_response"} else "general_response"
    #print(f"Decision made by decide_and_execute: {state}")

    # Save updated state to memory
    memory.save_context({"input": user_input}, {"output": decision})

    # Ensure state is passed correctly
    return state

