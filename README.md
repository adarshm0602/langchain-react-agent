# LangChain ReAct Agent with Claude

A Python-based ReAct (Reasoning + Acting) agent built with [LangChain](https://www.langchain.com/) and Anthropic's [Claude Haiku](https://www.anthropic.com/) model. The agent reasons step-by-step through complex questions, selecting the right tool for each sub-task and combining results into a final answer.

## What is a ReAct Agent?

ReAct is a prompting pattern where an LLM iterates through a **Thought → Action → Observation** loop:

1. **Thought** — The model reasons about what it needs to do next.
2. **Action** — It picks a tool and provides input.
3. **Observation** — It reads the tool's output.
4. **Repeat** until it has enough information to produce a **Final Answer**.

This lets the agent break down multi-part questions, use external tools for tasks it can't do reliably on its own (like arithmetic), and chain results together.

## Tools

The agent has access to three custom tools:

| Tool | Description | Example Input |
|------|-------------|---------------|
| **calculator** | Evaluates a Python math expression | `1200000 * 0.3` |
| **unit_converter** | Converts km to miles or kg to lbs | `100 km` |
| **word_counter** | Counts the number of words in a sentence | `Hello world` |

## Project Structure

```
langchain-react-agent/
├── agent.py           # Agent definition, tools, and main entry point
├── requirements.txt   # Python dependencies
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/langchain-react-agent.git
cd langchain-react-agent
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Set your Anthropic API key

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

You can get an API key from the [Anthropic Console](https://console.anthropic.com/).

### 4. Run the agent

```bash
python3 agent.py
```

## Example Output

The agent is pre-loaded with this question:

> *"If Bengaluru has a population of 12 million and 30% are tech workers, how many is that? Also convert 100 km to miles."*

```
> Entering new AgentExecutor chain...
Thought: I need to answer two questions:
1. Calculate 30% of 12 million
2. Convert 100 km to miles

Action: calculator
Action Input: 12000000 * 0.3
Observation: 3600000.0

Thought: Now I need to convert 100 km to miles.

Action: unit_converter
Action Input: 100 km
Observation: 100.0 km = 62.1371 miles

Final Answer:
- 30% of 12 million = 3.6 million tech workers
- 100 km = 62.14 miles

> Finished chain.
```

## How It Works

1. **LLM** — `ChatAnthropic` initializes Claude Haiku with `temperature=0` for deterministic reasoning.
2. **Tools** — Three functions decorated with `@tool` are registered with the agent. LangChain uses each tool's docstring as its description so the model knows when to use it.
3. **Agent** — `initialize_agent` wires the LLM and tools together using the `ZERO_SHOT_REACT_DESCRIPTION` agent type, which implements the ReAct loop with no few-shot examples.
4. **Execution** — `agent.invoke()` sends the question to the agent, which iterates through Thought/Action/Observation cycles until it reaches a final answer.

## Dependencies

- **langchain** — Agent framework and orchestration
- **langchain-anthropic** — Claude model integration
- **langchain-community** — Community tool and utility support
