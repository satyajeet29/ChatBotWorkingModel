from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def SQLdecide_and_execute(state, llm, schemaContext, sqlPromptTemplate, memory, supabase, formatType="json"):
    # Run chain to get response
    #print("SQL Supervisor Trigerred")
    user_query = state["user_input"]
    prompt_template = PromptTemplate(
        input_variables=["history", "user_query"],
        template=""" Classify the user query into one of the following Greenbuilding domains:
                        - 'User and Property Access'
                        - 'Energy Consumption and Utility Data'
                        - 'Anomaly Detection'
                        - 'Document and Data Storage'
                        - 'Benchmarking and Energy Models'
                        - 'Weather Data'
                
                Examples:
                        - "What properties do I have access to?" → 'User and Property Access'
                        - "Can I make changes to Property X?" → 'User and Property Access'
                        - "Why can’t I see Property Y?" → 'User and Property Access'
                        - "What is the energy consumption for Property X this month?" → 'Energy Consumption and Utility Data'
                        - "Which system of property Y is taking more energy?" → 'Energy Consumption and Utility Data'
                        - "How was my energy consumption for Month A this year compared to Month A last year?" → 'Energy Consumption and Utility Data'
                        - "Which facade of Property X needs immediate attention?" → 'Anomaly Detection'
                        - "What are the critical points that I need to address?" → 'Anomaly Detection'
                        - "What anomalies have been found for property A?" → 'Anomaly Detection'
                        - "Where can I upload documents for Property X?" → 'Document and Data Storage'
                        - "How many floors are there in building X?" → 'Document and Data Storage'
                        - "Where does my building stand in comparison to other buildings of the same size?" → 'Benchmarking and Energy Models'
                        - "Has my Energy Star score improved over time?" → 'Benchmarking and Energy Models'
                        - "What is the payback period for [X energy conservation measure] ?" → 'Benchmarking and Energy Models'
                        - "What is the forecasted weather for Property X?" → 'Weather Data'
                        - "What was the average monthly weather data for Property Y?" → 'Weather Data'                
        
                Only return one of the domain-specific categories listed above.
                
                
                Previous conversation: {history}

                User query: "{user_query}"

                Provide a response with only the category name (e.g., 'User and Property Access') and no additional text or formatting.
                 """
    )


    # Create LLM chain
    chain = LLMChain(llm=llm, prompt=prompt_template, memory=memory)


    response = chain.run({"history": memory.load_memory_variables({})["history"], "user_query": user_query}).strip()

    # Ensure the response matches one of the domain names
    valid_domains = [
        'User and Property Access', 'Energy Consumption and Utility Data',
        'Anomaly Detection', 'Document and Data Storage',
        'Benchmarking and Energy Models', 'Weather Data'
    ]
    if response not in valid_domains:
        response = "general_responseFurther"  # Default response if invalid

    # Save conversation to memory
    memory.save_context({"input": user_query}, {"output": response})

    # return response
    # Ensure the response is properly stored in 'messages'
    messages = state.get("messages", [])  # Retrieve existing messages or initialize
    messages.append({"role": "assistant", "content": response})  # Append latest response

    return {
        "user_input": user_query,
        "messages": messages,  # Ensure messages is updated
    }