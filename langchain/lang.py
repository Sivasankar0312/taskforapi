from langchain_community.utilities import SQLDatabase
from pydantic import BaseModel, PydanticUserError
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDatabaseTool,
)
from fastapi import FastAPI, HTTPException

app = FastAPI()
db = SQLDatabase.from_uri("sqlite:///financial_data.db")
print(db.dialect)
print(db.get_usable_table_names())
print(db.run("SELECT * FROM financial_data LIMIT 10;"))

llm = ChatAnthropic(model='claude-3-opus-20240229',api_key='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')


toolkit = SQLDatabaseToolkit(db=db, llm=llm)
print(toolkit.get_tools())
from langchain import hub

prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

assert len(prompt_template.messages) == 1
print(prompt_template.input_variables)
system_message = prompt_template.format(dialect="SQLite", top_k=5)
from langgraph.prebuilt import create_react_agent

agent_executor = create_react_agent(llm, toolkit.get_tools(), prompt=system_message)
example_query = "Which country's has least gdp values?"

events = agent_executor.stream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()
class QueryRequest(BaseModel):
    query: str


@app.get("/")
def read_root():
    return {"message": "Welcome to the LLM-powered SQL Agent API"}
@app.post("/query/")
async def query_data(request: QueryRequest):
    query = request.query

    try:
        events = agent_executor.stream(
            {"messages": [("user", query)]},
            stream_mode="values",
        )
        
        # Collect the events and send back the response
        result = []
        for event in events:
            result.append(event["messages"][-1].pretty_print())
        
        return {"result": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the query: {str(e)}")


# Example: Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)