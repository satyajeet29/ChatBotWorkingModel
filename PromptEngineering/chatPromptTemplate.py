from langchain.prompts import ChatPromptTemplate

def sqlPromptTemplate(schemaContext):
    return ChatPromptTemplate.from_template(
        schemaContext +
        """
        Based on the schema above, generate an optimized SQL query:
        User Question: {query}
        SQL:
        ```sql
        """
    )