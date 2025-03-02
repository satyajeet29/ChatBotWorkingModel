from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def genericResponse(user_query, llm, memory):
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

    return response