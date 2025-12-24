import os
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

load_dotenv()

os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(model="gpt-4.1-mini", temperature=0.3)

@tool("take_orders", description="Use this when the customer finishes their order")
def take_orders()-> str:
    return f"Your order has been placed"

prompt = (
    "You are an agent that takes in a transcript generated from a voice ai there might be some words that the agent does not capture correctly"
    "The customer might try to make small talk with you answer properly but keep to the task at hand"
    "You are to make use of your discretion to understand the sentence and make sure your understanding is contextually and gramatically correct so you can properly understand it."
    "Your reply should be humorous with proper punctuations and spaces as it would be fed into a voice ai model"
    "Only after the user make an order are you allowed to make sure to ask the user if they will want to make an extra order of it that will be all."   

)
agent = create_agent(
    model = model,
    tools = [take_orders],
    checkpointer= InMemorySaver(),
    system_prompt= prompt
)

thread_id = "customer_pipeline"
# orders = "How are you doing today"


def ask_agent(transcript:str) -> str:
    """Send transcript to agent and get response text."""
    response = agent.invoke({
        "messages": 
        [{"role" : "user", "content" : transcript }]
    },
    config={"configurable": {"thread_id": thread_id}}
    )

    messages = response["messages"]
    for msg in reversed(messages):
        if msg.type == "ai":
            return msg.content
    return "Sorry, I could not understand"