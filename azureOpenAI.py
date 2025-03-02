import os
from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI

def azureOpenAI(apiKey, version, endpoint):
    return AzureOpenAI(
        api_key=apiKey,
        api_version=version,
        azure_endpoint=endpoint
    )
def azureChatOpenAI():
    return AzureChatOpenAI(
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0
        )