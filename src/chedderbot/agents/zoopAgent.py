from langchain.agents import create_react_agent, AgentExecutor


def create_zoop_agent(model, tools, prompt):
    agent = create_react_agent(model, tools, prompt)

    zoop_agent = AgentExecutor.from_agent_and_tools(
        agent = agent,
        tools = tools,
        verbose = True,
        handle_parsing_errors = True
    )

    return zoop_agent