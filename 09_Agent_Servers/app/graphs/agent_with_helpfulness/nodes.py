from app.graphs.agent_with_helpfulness.agent_state import AgentState
from app.models import get_chat_model
from app.tools import get_tool_belt
from app.models import get_judge_model
from langgraph.graph import END
from langchain_core.messages import HumanMessage

MAX_RETRIES = 2
RETRY = "retries"

SYSTEM_PROMPT = (
    "You are a helpful assistant specialized in feline (cat) health. "
    "Use the retrieve_information tool for cat-health questions, web search for "
    "current information, and Arxiv for research papers. Cite tool results when "
    "they inform your answer."
)

JUDGE_PROMPT = """
You are a helpful judge specialized in evaluating the helpfulness of an assistant's response to a user's question.

The assistant's response is:
{response}

The user's question is:
{question}

Was the assistant's response helpful?
Return ONLY: YES or NO.
"""

def initialize(state: AgentState) -> dict:
    return {
        "retries": 0,
        "helpfulness": None,
    }

def agent(state: AgentState) -> dict:
    llm_with_tools = get_chat_model().bind_tools(get_tool_belt())
    response = llm_with_tools.invoke(
        [{"role": "system", "content": SYSTEM_PROMPT}, *state["messages"]]
    )
    return {"messages": [response]}


def helpfulness_judge(state: AgentState) -> dict:
    answer = state["messages"][-1].content
    question = None
    for message in reversed(state["messages"]):
        if isinstance(message,HumanMessage):
            question = message.content
            break

    response = get_judge_model().invoke(
        [{"role": "user", "content": JUDGE_PROMPT.format(response=answer, question=question)}]
    )

    helpfulness = str(response.content).strip().lower() == "yes"
    return {"helpfulness": helpfulness}


def retries(state: AgentState) -> dict:
    return {"retries": state["retries"] + 1}

def route_after_helpfulness_judge(state: AgentState) -> str:
    if state["helpfulness"]:
        return END
    
    if state["retries"] >= MAX_RETRIES:
        return END
    
    return RETRY
    