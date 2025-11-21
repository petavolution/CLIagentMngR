# eats_core - Simplified EATS Implementation
"""
EATS Core: Evolutionary Agent Tree System

Optimized hackathon version consolidating:
- Unified transport (PTY + tmux)
- Agent DNA/evolution
- Hierarchical swarm control
- LLM-as-judge fitness
- Result aggregation
"""

from .core import (
    Transport,
    PTYTransport,
    TmuxTransport,
    AgentDNA,
    Agent,
    Evolution,
)
from .swarm import SwarmController, TreeNode, BranchType
from .judge import LLMJudge, Fitness
from .pipeline import ResultPipeline, FusedOutput
from .server import create_app, run_server

__version__ = "2.0.0-hackathon"
__all__ = [
    "Transport",
    "PTYTransport",
    "TmuxTransport",
    "AgentDNA",
    "Agent",
    "Evolution",
    "SwarmController",
    "TreeNode",
    "BranchType",
    "LLMJudge",
    "Fitness",
    "ResultPipeline",
    "FusedOutput",
    "create_app",
    "run_server",
]
