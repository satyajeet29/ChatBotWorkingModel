from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def genericResponse(state, llm, memory):
    user_query = state["user_input"]
    """Use LLM to generate a generic response for user queries that don't require SQL."""
    # Define prompt template
    prompt_template = PromptTemplate(
        input_variables=["history", "user_query"],
        template="""
          You are an intelligent assistant for green building management. Answer the following user query clearly and concisely.

          Previous conversation: {history}

          User query: "{user_query}"

          Provide a well-structured response.
          """
    )
    # Create LLM chain
    chain = LLMChain(llm=llm, prompt=prompt_template, memory=memory)

    # Run chain to get response
    response = chain.run({"history": memory.load_memory_variables({})["history"], "user_query": user_query}).strip()

    # Save conversation to memory
    memory.save_context({"input": user_query}, {"output": response})

    #return response
    # Ensure the response is properly stored in 'messages'
    messages = state.get("messages", [])  # Retrieve existing messages or initialize
    messages.append({"role": "assistant", "content": response})  # Append latest response

    return {
            "user_input": user_query,
            "messages": messages,  # Ensure messages is updated
        }