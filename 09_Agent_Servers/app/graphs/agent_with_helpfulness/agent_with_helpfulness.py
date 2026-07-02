from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from app.graphs.agent_with_helpfulness.nodes import initialize
from app.tools import get_tool_belt
from app.graphs.agent_with_helpfulness.nodes import (
    agent,
    helpfulness_judge,
    retries,
    route_after_helpfulness_judge,
)
from app.graphs.agent_with_helpfulness.agent_state import AgentState

langgraph_builder = StateGraph(AgentState)
langgraph_builder.add_node("agent", agent)
langgraph_builder.add_node("initialize", initialize)
langgraph_builder.add_node("tools", ToolNode(get_tool_belt()))
langgraph_builder.add_node("helpfulness_judge", helpfulness_judge)
langgraph_builder.add_node("retries", retries)
langgraph_builder.add_edge(START, "initialize")
langgraph_builder.add_edge("initialize", "agent")
langgraph_builder.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: "helpfulness_judge"})
langgraph_builder.add_edge("tools", "agent")
langgraph_builder.add_edge("retries", "agent")
langgraph_builder.add_conditional_edges("helpfulness_judge", 
route_after_helpfulness_judge, path_map={END: END, "retries": "retries"})

compiled_graph = langgraph_builder.compile()
