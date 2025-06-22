from langchain.tools import OpenAPITool
from langchain.agents import initialize_agent


tool = OpenAPITool.from_openapi_url(
    name="example",
    url="http://localhost:8123/openapi.json",
)
agent = initialize_agent([tool], llm=None, agent="zero-shot-react-description")
print(agent.run("Return the current time"))
