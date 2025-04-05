# 🔴 Note: This item is still in progress and as of now it has been able to direct the query to it's respective domain 
### 1.0: Steps to make it work on your system:
<details>
   <summary style="color: green; font-weight: bold;">Ordered list of steps (Click to expand)</summary>
   <pre>
    <span>1. Please download the given folder</span>
    <span>2. Add a .env file with following variables to project folder listed below in section 2.0</span> 
    <span >3. Open a terminal and navigate to the project folder and execute: python AppLangGraphTooled.py </span>
   </pre>
</details>

### 2.0: .env variable details:
<details>
  <summary style="color: green; font-weight: bold;">🔐 Environment Variables (Click to expand)</summary>
  <pre>
  <span style="color: orange;">LANGSMITH_TRACING=true</span>
  <span style="color: red;">LANGSMITH_API_KEY=</span>
  <span style="color: red;">AZURE_OPENAI_API_KEY=</span>
  <span style="color: blue;">AZURE_OPENAI_ENDPOINT=https://msa-openai.openai.azure.com/</span>
  <span style="color: purple;">AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o</span>
  <span style="color: purple;">AZURE_OPENAI_API_VERSION=2023-12-01-preview</span>
  <span style="color: orange;">subapase_email=</span>
  <span style="color: orange;">subapase_password=</span>
  <span style="color: green;">SUPABASE_URL=</span>
  <span style="color: green;">SUPABASE_KEY=</span>
  </pre>
</details>

### 3.0: Description of the architecture
   Based on the number of business domains involved along with a requirement to have contextual communication we have adopted a Supervisor based architecture further followed by a sub-supervisor to direct domain specific queries to respective domains to generate response for that specific domain, we did use a memory variable to maintain the state and history of queries, using which further context around ongoing query can be maintained to help facilitate a more meaningful conversation as a green building chat bot. 
#### 3.1 List of components:
- Supervisor1: Determines if the user query is a domain specific query that needs to be directed towards the Generic LLM if the given query is generic in nature and isn’t pertaining to the five domains listed under Supervisor 2  
   - Generic LLM: It focuses on answering generic questions as a greenbuilding chatbot 
   - Supervisor 2: Based on user queries it determines which domain it would be further directed to following SQL based agents: 
      - User Property: Focuses on determining which properties a user has with read/write access 
      - Energy Consumption: Assist in determination of energy consumption for a given property a user has access to, followed by ability to identify high energy consuming system and computation of average energy consumption 
      - Anomaly: Utilize available anomaly tables to determine properties needing immediate attention 
      - Document Data Storage: Locate documents to a given property along with obtaining real estate information around it 
      - Benchmarking Energy: Compute energy benchmarks across properties based on energy followed by computation of energy star score 
      - Weather Data: Helps determine weather related values associated with a given property 
- Bot response: Acts as the outlet for an information generated from the workflow above 
#### 3.2 How is the domain being infered
The prior list of queries provided to us were used for creating a text vector mapping to let the Supervisor 2 infer the domain(path: ChatBotHelper/SQLSupervisor.py ):
- Examples:
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

### 4.0: Output values

### 5.0: Next Steps

### 6.0


