from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def SQLdecide_and_execute(state, llm, schemaContext, sqlPromptTemplate, memory, supabase, formatType="json"):
    user_input = state["user_input"]
    prompt_template = PromptTemplate(
        input_variables=["history", "user_query"],
        template="""
                 You are an AI assistant that classifies user queries into one of the following domains:
                     1. User and Property Access
                     2. Energy Consumption and Utility Data
                     3. Anomaly Detection
                     4. Document and Data Storage
                     5. Benchmarking and Energy Models
                     6. Weather Data

                 Previous conversation: {history}

                 User query: "{user_query}"

                 Provide a response with the category number and name in the following format:
                    <number>. <name>
                 """
    )
