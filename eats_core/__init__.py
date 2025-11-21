# eats_core - Simplified EATS Implementation
"""
EATS Core: Evolutionary Agent Tree System

Optimized hackathon version v2.1 with enhanced modules:

Core (core.py):
- Unified transport (PTY + tmux)
- Agent DNA/evolution
- Built-in fitness functions

Async (async_core.py):
- Concurrent agent execution
- Worker pools with rate limiting
- Orchestrator-worker pattern

Swarm (swarm.py):
- Hierarchical agent tree
- Probability-fan spawning
- Senescence tracking

Judge (judge.py):
- LLM-as-judge fitness
- Pairwise comparison
- Hybrid scoring

Pipeline (pipeline.py):
- DAG result trees
- Fusion methods
- Semantic caching

Events (events.py):
- Real-time pub/sub
- SSE streaming
- Event decorators

Workflows (workflows.py):
- DAG-based workflows
- Prompt chaining
- Parallel execution

Presets (presets.py):
- Agent archetypes
- Team configurations
- Optimized prompts

Persistence (persistence.py):
- State snapshots
- DNA library
- Export/import

Metrics (metrics.py):
- Performance tracking
- Cost estimation
- Observability

Server (server.py):
- FastAPI server
- Dashboard UI
- CLI interface
"""

__version__ = "2.1.0"

# Core components
from .core import (
    Transport,
    PTYTransport,
    TmuxTransport,
    AgentDNA,
    Agent,
    Evolution,
    EvolutionConfig,
    heuristic_fitness,
)

# Swarm management
from .swarm import (
    SwarmController,
    TreeNode,
    BranchType,
    AgentRole,
    fan_layout,
    grid_layout,
)

# Fitness evaluation
from .judge import (
    LLMJudge,
    Fitness,
    Criterion,
    create_fitness_fn,
    create_keyword_fitness,
    create_code_fitness,
)

# Result processing
from .pipeline import (
    ResultPipeline,
    FusedOutput,
    FusionMethod,
)

# Async execution
from .async_core import (
    AsyncAgent,
    TaskResult,
    WorkerPool,
    AsyncEvolution,
    AsyncEvolutionConfig,
    OrchestratorWorker,
    run_parallel,
    run_with_taskgroup,
    run_first_wins,
    create_agent_pool,
    shutdown_agents,
)

# Event system
from .events import (
    Event,
    EventType,
    EventBus,
    EventStream,
    EventEmitter,
    get_event_bus,
    emit,
    on_event,
    emits,
)

# Workflows
from .workflows import (
    Workflow,
    WorkflowBuilder,
    WorkflowNode,
    NodeType,
    NodeStatus,
    create_chain_workflow,
    create_parallel_workflow,
)

# Agent presets
from .presets import (
    AgentPreset,
    PresetCategory,
    get_preset,
    list_presets,
    search_presets,
    create_dna,
    get_team,
    create_team_dna,
    ALL_PRESETS,
    TEAMS,
    # Individual presets
    CODER,
    REVIEWER,
    TESTER,
    DEBUGGER,
    PLANNER,
    ORCHESTRATOR,
)

# Persistence
from .persistence import (
    Storage,
    MemoryStorage,
    FileStorage,
    StateManager,
    Snapshot,
    get_state_manager,
    save,
    load,
)

# Metrics
from .metrics import (
    MetricsRegistry,
    EATSMetrics,
    Counter,
    Gauge,
    Histogram,
    Timer,
    get_metrics,
)

# Server
from .server import (
    create_app,
    run_server,
    run_cli,
)

__all__ = [
    # Version
    "__version__",
    # Core
    "Transport",
    "PTYTransport",
    "TmuxTransport",
    "AgentDNA",
    "Agent",
    "Evolution",
    "EvolutionConfig",
    "heuristic_fitness",
    # Swarm
    "SwarmController",
    "TreeNode",
    "BranchType",
    "AgentRole",
    "fan_layout",
    "grid_layout",
    # Judge
    "LLMJudge",
    "Fitness",
    "Criterion",
    "create_fitness_fn",
    "create_keyword_fitness",
    "create_code_fitness",
    # Pipeline
    "ResultPipeline",
    "FusedOutput",
    "FusionMethod",
    # Async
    "AsyncAgent",
    "TaskResult",
    "WorkerPool",
    "AsyncEvolution",
    "AsyncEvolutionConfig",
    "OrchestratorWorker",
    "run_parallel",
    "run_with_taskgroup",
    "run_first_wins",
    "create_agent_pool",
    "shutdown_agents",
    # Events
    "Event",
    "EventType",
    "EventBus",
    "EventStream",
    "EventEmitter",
    "get_event_bus",
    "emit",
    "on_event",
    "emits",
    # Workflows
    "Workflow",
    "WorkflowBuilder",
    "WorkflowNode",
    "NodeType",
    "NodeStatus",
    "create_chain_workflow",
    "create_parallel_workflow",
    # Presets
    "AgentPreset",
    "PresetCategory",
    "get_preset",
    "list_presets",
    "search_presets",
    "create_dna",
    "get_team",
    "create_team_dna",
    "ALL_PRESETS",
    "TEAMS",
    "CODER",
    "REVIEWER",
    "TESTER",
    "DEBUGGER",
    "PLANNER",
    "ORCHESTRATOR",
    # Persistence
    "Storage",
    "MemoryStorage",
    "FileStorage",
    "StateManager",
    "Snapshot",
    "get_state_manager",
    "save",
    "load",
    # Metrics
    "MetricsRegistry",
    "EATSMetrics",
    "Counter",
    "Gauge",
    "Histogram",
    "Timer",
    "get_metrics",
    # Server
    "create_app",
    "run_server",
    "run_cli",
]
