from PromptSection.DatabaseList import tableList
from PromptSection.UserPropertyAccessRules import userPropertyAccessRules
from PromptSection.ProjectAccessRules import projectAccessRules
from PromptSection.HandleBooleanValues import handleBooleans
def generateSchemaContext():
    SCHEMA_CONTEXT = f"""
    # **You are an AI assistant helping users retrieve data from a Supabase database meant for monitoring building energy levels**
    The database has 50 tables, including:
    '{tableList()}'
    # **Use this context to generate SQL queries.
    ## **List of business rules that would be useful for generating SQL queries**
    '{userPropertyAccessRules()}'
    '{projectAccessRules()}' 
    '{handleBooleans()}'
    """
    return SCHEMA_CONTEXT