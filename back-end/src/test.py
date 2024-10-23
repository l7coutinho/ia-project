from langchain import hub
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools import YouTubeSearchTool
from langchain_community.tools.google_trends import GoogleTrendsQueryRun
from langchain_community.utilities.google_trends import GoogleTrendsAPIWrapper
from langchain.agents import create_openai_functions_agent, AgentExecutor

load_dotenv()

#tools
youtube_tool = YouTubeSearchTool()
google_trends = GoogleTrendsQueryRun(api_wrapper=GoogleTrendsAPIWrapper())

print(youtube_tool.run("Neymar no YouTube"))

tools = [youtube_tool, google_trends]

#prompt
prompt = hub.pull("hwchase17/openai-functions-agent")

#llm
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

#agents
agent = create_openai_functions_agent(llm, tools, prompt)

#executar os agents
agent_executor = AgentExecutor(
	agent=agent,
	tools=tools,
	verbose=True,
)

agent_executor.invoke({ "input": "Neymar no YouTube" })
