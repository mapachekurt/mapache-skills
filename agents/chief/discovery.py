"""
Subagent Discovery Service for Chief

Scans the local filesystem (for testing) or environment-specified
locations for A2A agent.json profiles.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AgentDiscovery:
    """Discovers available agents and their capabilities"""
    
    def __init__(self, search_path: str = "."):
        self.search_path = Path(search_path)
        self.registry: Dict[str, Dict[str, Any]] = {}

    def scan(self) -> Dict[str, Dict[str, Any]]:
        """
        Scans for agent.json files in subdirectories of search_path.
        Returns a mapping of agent_id to their profile data.
        """
        logger.info(f"Scanning for agents in {self.search_path.absolute()}")
        
        # Look for agent.json in all subdirectories
        for json_file in self.search_path.glob("**/agent.json"):
            # Avoid picking up chief's own agent.json if it is in the same path
            # or picking up files that are not in a reasonable structure
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                    agent_id = profile.get("id")
                    if agent_id:
                        self.registry[agent_id] = profile
                        logger.info(f"Discovered agent: {agent_id} at {json_file}")
            except Exception as e:
                logger.error(f"Failed to parse {json_file}: {e}")
        
        return self.registry

    def get_capabilities_summary(self) -> str:
        """Returns a string description of all discovered agent capabilities for LLM prompt"""
        summary = []
        for agent_id, profile in self.registry.items():
            name = profile.get("name", agent_id)
            desc = profile.get("description", "No description")
            caps = ", ".join(profile.get("capabilities", []))
            summary.append(f"- Agent: {name} (ID: {agent_id})\n  Description: {desc}\n  Capabilities: {caps}")
        
        return "\n".join(summary)
