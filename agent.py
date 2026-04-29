import os

from langchain.agents import AgentType, initialize_agent
from langchain_anthropic import ChatAnthropic
from langchain.tools import tool


@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression. Input should be a valid Python math expression like '1200000 * 0.3'."""
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


@tool
def unit_converter(query: str) -> str:
    """Convert units. Supports 'km to miles' and 'kg to lbs'. Input format: '<number> <unit>' e.g. '100 km' or '50 kg'."""
    parts = query.strip().split()
    if len(parts) != 2:
        return "Error: Input must be '<number> <unit>', e.g. '100 km' or '50 kg'"
    try:
        value = float(parts[0])
    except ValueError:
        return f"Error: '{parts[0]}' is not a valid number"
    unit = parts[1].lower()
    if unit == "km":
        return f"{value} km = {value * 0.621371:.4f} miles"
    elif unit == "kg":
        return f"{value} kg = {value * 2.20462:.4f} lbs"
    else:
        return f"Error: unsupported unit '{unit}'. Supported: km, kg"


@tool
def word_counter(sentence: str) -> str:
    """Count the number of words in a sentence. Input should be a sentence or phrase."""
    count = len(sentence.split())
    return f"The sentence has {count} words."


def main():
    llm = ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        api_key=os.environ["ANTHROPIC_API_KEY"],
        temperature=0,
    )

    tools = [calculator, unit_converter, word_counter]

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    question = (
        "If Bengaluru has a population of 12 million and 30% are tech workers, "
        "how many is that? Also convert 100 km to miles."
    )

    result = agent.invoke({"input": question})
    print("\nFinal Answer:", result["output"])


if __name__ == "__main__":
    main()
