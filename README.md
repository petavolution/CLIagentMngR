# EATS - Evolutionary Agent Tree System

A biologically-inspired multi-agent orchestration framework for terminal-driven LLM coding agents.

## EATS Core v2.0 (Optimized)

The `eats_core/` directory contains a **simplified, optimized rewrite** of EATS consolidating:

- **Unified Transport** (`core.py`): PTY + tmux in single abstraction
- **Agent DNA/Evolution** (`core.py`): Genetic algorithms with minimal boilerplate
- **Hierarchical Swarm** (`swarm.py`): Tree-based multi-agent with senescence
- **LLM Judge** (`judge.py`): Pairwise comparison, position bias mitigation
- **Result Pipeline** (`pipeline.py`): DAG-based aggregation with fusion
- **API + CLI** (`server.py`): FastAPI server with embedded dashboard

### Quick Start (v2.0)

```bash
# Run demo
python run_core.py demo

# Start API server at http://localhost:8000
python run_core.py server

# Interactive CLI
python run_core.py cli
```

### Minimal Dependencies

Core functionality has **zero external dependencies**. Optional:
- `fastapi` + `uvicorn` for web server
- `libtmux` for tmux transport
- `rich` for pretty CLI output

---

## Overview

EATS enables you to:
- **Spawn multiple LLM CLI agents** in parallel terminal sessions (PTY or tmux)
- **Evolve agent configurations** using genetic algorithms (mutation, crossover, selection)
- **Visualize the agent tree** in real-time via enhanced web UI with dagre layout
- **LLM-as-judge fitness evaluation** for sophisticated quality assessment
- **Hierarchical agent trees** with Research/Creative/Execution branches
- **GhostSwarm mode** for visual multi-terminal orchestration
- **Human-supervised control** - you stay in the loop

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MultiAgentOrchestrator                           │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────────┐ │
│  │ MetaManager  │  │ EvoEngine    │  │ HierarchicalAgentTree      │ │
│  │ (sessions)   │  │ (genetics)   │  │ (Research/Creative/Exec)   │ │
│  └──────┬───────┘  └──────┬───────┘  └────────────┬───────────────┘ │
│         │                 │                       │                 │
│  ┌──────┴─────────────────┴───────────────────────┴───────────────┐ │
│  │ OrchestrationGraph + OutputProcessor + EventBus                │ │
│  └────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
   ┌────┴────┐             ┌────┴────┐             ┌────┴────┐
   │ Agent 1 │             │ Agent 2 │             │ Agent N │
   │ (PTY)   │             │ (tmux)  │             │ (PTY)   │
   └─────────┘             └─────────┘             └─────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
cd project1
pip install -r requirements.txt
```

### 2. Run the Web Server

```bash
./run_server.sh
# or
python -m uvicorn eats.api:app --reload --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000 in your browser.

### 3. CLI Supervisor

```bash
./run_cli.sh
# or
python -m eats.cli_supervisor
```

### 4. GhostSwarm (Visual Multi-Terminal)

```bash
python -m eats.ghost_swarm --agents 4 --layout fan
```

## Usage

### Enhanced Web UI

The web UI features:
- **Dagre layout** for hierarchical agent visualization
- **Real-time updates** via Server-Sent Events
- **Fitness charts** showing evolution progress
- **Agent inspection panel** with conversation logs
- **Interactive graph** - click agents to inspect

### CLI Supervisor Commands

```
eats> spawn coder           # Spawn a coder agent
eats> agents                # List all agents
eats> select abc123         # Select agent by ID prefix
eats> prompt Write hello.py # Send prompt to selected agent
eats> tail                  # View last output
eats> log                   # View conversation history
eats> task Sort a list      # Create a task
eats> evolve 3              # Run 3 generations of evolution
eats> fitness               # View fitness across generations
eats> graph                 # View agent tree structure
eats> status                # System status
eats> reset                 # Reset all agents
eats> quit                  # Exit
```

### GhostSwarm Commands

```
ghost> list                 # List all agents in swarm
ghost> send Coder_Alpha msg # Send to specific agent
ghost> broadcast msg        # Send to all agents
ghost> read Coder_Alpha     # Read agent's output
ghost> status               # Show status table
ghost> quit                 # Exit
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

# Stream events (SSE)
curl http://localhost:8000/events
```

## Project Structure

```
eats/
├── __init__.py           # Package init
├── transport_pty.py      # PTY-based terminal control
├── tmux_transport.py     # Tmux/GhostSwarm transport with GUI windows
├── agents.py             # AgentSession, Turn classes
├── config_models.py      # Blueprint, Task, Config dataclasses
├── manager.py            # MetaManager (agent registry)
├── event_bus.py          # Pub/sub event system
├── task_graph.py         # Orchestration graph for visualization
├── hierarchical_tree.py  # Research/Creative/Execution branches
├── evolution_engine.py   # Genetic algorithm (mutation, selection)
├── output_processor.py   # DAG result trees, semantic caching
├── llm_judge.py          # LLM-as-judge fitness evaluation
├── orchestrator.py       # High-level coordination
├── api.py                # FastAPI server
├── cli_supervisor.py     # Interactive CLI
└── ghost_swarm.py        # Visual multi-terminal controller

static/
└── index.html            # Enhanced web UI with dagre layout
```

## Key Concepts

### Agent Blueprint (DNA)
The genetic material of an agent:
- **Phenotype**: Role, system prompt, tool access
- **Genotype**: Temperature, top-p, context configuration

### Hierarchical Agent Tree
```
Meta-Orchestrator (Root)
├── Research Branch
│   ├── Web Search Agents
│   ├── Document Analysis Agents
│   └── Synthesis Agent
├── Creative Branch
│   ├── Text Generators
│   ├── Image Coordinators
│   └── Multimodal Fusion Agent
└── Execution Branch
    ├── Code Executors
    ├── File System Agents
    └── QA Agent
```

### Fitness Functions
- `combined_fitness`: Multi-factor evaluation (length, code, explanations, speed)
- `keyword_fitness`: Presence of expected keywords
- `create_llm_judge_fitness()`: LLM-as-judge evaluation
- `create_hybrid_fitness()`: Combined LLM + heuristic

### Evolution Cycle
1. Create initial population from base blueprint
2. Spawn agents and evaluate on task
3. **LLM-as-judge** scores responses on correctness, clarity, efficiency
4. Select top 20%, prune bottom 10%
5. Mutate (prompt drift, temperature variation) + crossover
6. Repeat with **senescence tracking** for performance decay

### Output Processing Pipeline
- **Semantic cache**: Avoid redundant processing
- **DAG result tree**: Track output lineage
- **Fusion methods**: Ensemble voting, weighted synthesis, hierarchical roll-up

### GhostSwarm Visual Layout
- **Probability Fan (Wahrscheinlichkeitsfächer)**: Windows arranged in fan pattern
- **Grid Layout**: Windows in rows/columns
- **Hierarchy Layout**: Tree-based positioning

## Configuration

### Using Real LLM CLIs

Edit `eats/api.py` and change `DEFAULT_AGENT_CMD`:

```python
# For Aider
DEFAULT_AGENT_CMD = ["aider"]

# For Open Interpreter
DEFAULT_AGENT_CMD = ["interpreter"]

# For GPT4All
DEFAULT_AGENT_CMD = ["gpt4all", "--model", "path/to/model.gguf"]

# For Claude Code
DEFAULT_AGENT_CMD = ["claude"]
```

### Evolution Parameters

```python
EvolutionConfig(
    population_size=4,              # Agents per generation
    top_k_survivors=2,              # How many survive
    mutation_rate=0.2,              # Probability of mutation
    prompt_mutation_strength=0.1,   # How much to perturb prompts
    temperature_mutation_range=0.1, # Max temp change
    max_generations=5,              # Evolution iterations
    max_turn_seconds=30.0,          # Timeout per agent response
)
```

### GhostSwarm Options

```bash
python -m eats.ghost_swarm \
  --session my_swarm \
  --terminal alacritty \
  --agents 5 \
  --layout fan \
  --cmd aider
```

## 2026 Target Hardware

Optimized for home server deployment:
- GPU: RTX 5090 32GB GDDR7 (Llama 3.1 70B Q4, Flux Schnell)
- CPU: AMD Ryzen 9 9950X (16 core)
- RAM: 128 GB DDR5-6000
- SSD: 4 TB NVMe

## Future Extensions

- **SSH transport**: Spawn agents on remote servers via paramiko
- **VR visualization**: 3D agent tree in Godot/Unity
- **Image generation agents**: Multimodal workflows with ComfyUI
- **Vector embeddings**: Semantic similarity with sentence-transformers
- **Redis messaging**: Distributed agent communication
- **vLLM integration**: High-performance local LLM serving

## License

MIT
