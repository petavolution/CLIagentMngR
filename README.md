# EATS - Evolutionary Agent Tree System

A biologically-inspired multi-agent orchestration framework for terminal-driven LLM coding agents.

## Overview

EATS enables you to:
- **Spawn multiple LLM CLI agents** in parallel terminal sessions
- **Evolve agent configurations** using genetic algorithms (mutation, selection)
- **Visualize the agent tree** in real-time via web UI
- **Human-supervised control** - you stay in the loop

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MultiAgentOrchestrator                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ MetaManager │  │ EvoEngine   │  │ OrchestrationGraph  │  │
│  │ (sessions)  │  │ (genetics)  │  │ (visualization)     │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                    │             │
│         └────────────────┴────────────────────┘             │
│                          │                                  │
│                    ┌─────┴─────┐                            │
│                    │ EventBus  │                            │
│                    └─────┬─────┘                            │
└──────────────────────────┼──────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────┴────┐       ┌────┴────┐       ┌────┴────┐
    │ Agent 1 │       │ Agent 2 │       │ Agent N │
    │ (PTY)   │       │ (PTY)   │       │ (PTY)   │
    └─────────┘       └─────────┘       └─────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
cd project1
pip install -r requirements.txt
```

### 2. Run the Web Server

```bash
python -m uvicorn eats.api:app --reload --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000 in your browser.

### 3. Or Use the CLI Supervisor

```bash
python -m eats.cli_supervisor
```

## Usage

### Web UI

1. **Spawn Agent**: Click "Spawn Agent" and enter a role (coder, tester, planner)
2. **Create Task**: Click "Create Task" and describe what you want solved
3. **Run Evolution**: Click "Run Evolution" to optimize agents for the task
4. **Watch**: See agents spawn, mutate, and evolve in the tree visualization

### CLI Supervisor

```
eats> spawn coder           # Spawn a coder agent
eats> agents                # List all agents
eats> select abc123         # Select agent by ID prefix
eats> prompt Write hello.py # Send prompt to selected agent
eats> tail                  # View last output
eats> task Sort a list      # Create a task
eats> evolve 3              # Run 3 generations of evolution
eats> fitness               # View fitness across generations
eats> status                # System status
eats> quit                  # Exit
```

### REST API

```bash
# Spawn agent
curl -X POST http://localhost:8000/agents \
  -H "Content-Type: application/json" \
  -d '{"role": "coder", "system_prompt": "You are helpful."}'

# List agents
curl http://localhost:8000/agents

# Send prompt
curl -X POST http://localhost:8000/agents/{id}/prompt \
  -H "Content-Type: application/json" \
  -d '{"text": "Write a sorting function"}'

# Create task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"description": "Write a binary search"}'

# Run evolution
curl -X POST http://localhost:8000/evolution/run \
  -H "Content-Type: application/json" \
  -d '{"task_id": "...", "population_size": 4, "max_generations": 3}'

# Get graph (Cytoscape.js format)
curl http://localhost:8000/graph
```

## Configuration

### Using a Real LLM CLI

Edit `eats/api.py` and change `DEFAULT_AGENT_CMD`:

```python
# For Aider
DEFAULT_AGENT_CMD = ["aider"]

# For Open Interpreter
DEFAULT_AGENT_CMD = ["interpreter"]

# For GPT4All
DEFAULT_AGENT_CMD = ["gpt4all", "--model", "path/to/model.gguf"]
```

### Evolution Parameters

Adjust in `EvolutionConfig`:

```python
EvolutionConfig(
    population_size=4,      # Agents per generation
    top_k_survivors=2,      # How many survive
    mutation_rate=0.2,      # Probability of mutation
    max_generations=5,      # Evolution iterations
    max_turn_seconds=30.0,  # Timeout per agent response
)
```

## Project Structure

```
eats/
├── __init__.py           # Package init
├── transport_pty.py      # PTY-based terminal control
├── agents.py             # AgentSession, Turn classes
├── config_models.py      # Blueprint, Task, Config dataclasses
├── manager.py            # MetaManager (agent registry)
├── event_bus.py          # Pub/sub event system
├── task_graph.py         # Orchestration graph for visualization
├── evolution_engine.py   # Genetic algorithm (mutation, selection)
├── orchestrator.py       # High-level coordination
├── api.py                # FastAPI server + web UI
└── cli_supervisor.py     # Interactive CLI
```

## Key Concepts

### Agent Blueprint
The "DNA" of an agent - includes system prompt, temperature, role. This is what gets mutated during evolution.

### Fitness Function
Evaluates how well an agent solves a task. Built-in functions:
- `combined_fitness`: Evaluates length, code presence, explanations, speed
- `keyword_fitness`: Checks for expected keywords
- `simple_length_fitness`: Basic length-based scoring (for testing)

### Evolution Cycle
1. Create initial population from base blueprint
2. Spawn agents and evaluate on task
3. Select top performers
4. Mutate/crossover to create next generation
5. Repeat

## Future Extensions

- **tmux transport**: Control agents via tmux panes
- **SSH transport**: Spawn agents on remote servers
- **VR visualization**: 3D agent tree in Godot/Unity
- **Image generation agents**: Multimodal workflows
- **Persistent memory**: Agent knowledge across sessions

## License

MIT
