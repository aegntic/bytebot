#!/usr/bin/env python3
"""
Agent Launcher for Sequential Thinking Swarm

Handles the launching and coordination of individual Claude CLI agents
that implement sequential thinking and ultrathink methodologies.
"""

import json
import os
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class AgentLauncher:
    """Manages launching and coordinating individual CLI agents"""

    def __init__(self, workspace_dir: str = "/tmp/swarm_workspace"):
        self.workspace_dir = Path(workspace_dir)
        self.active_processes = {}
        self.agent_configs = self._load_agent_configs()

    def _load_agent_configs(self) -> Dict[str, Dict[str, Any]]:
        """Load specialized configurations for each agent type"""

        return {
            "coordinator": {
                "description": "Orchestrates swarm activities and coordinates thinking sessions",
                "system_prompt": """You are the Coordinator Agent for a sequential thinking swarm.

Your role is to:
1. Orchestrateswarm activities and coordinate multi-agent thinking
2. Distribute tasks to specialized agents based on their expertise
3. Ensure sequential thinking methodology is followed at each step
4. Monitor progress and facilitate collaborative ultrathink sessions
5. Synthesize individual agent insights into coherent outputs

Always use the Systems-First Execution Framework:
- Phase 1: Map the problem space before acting
- Phase 2: Verify all assumptions with evidence
- Phase 3: Apply minimal intervention for maximum outcome

Communication: Use the file-based system in the workspace to coordinate with other agents.""",
                "tools": ["file_operations", "task_coordination"],
                "thinking_style": "meta_cognitive_orchestration"
            },

            "analyst": {
                "description": "Performs deep first-principles analysis and problem decomposition",
                "system_prompt": """You are the Analyst Agent specializing in deep sequential thinking and first-principles reasoning.

Your methodology follows FPEF rigorously:

**Phase 1: System Mapping (Mandatory)**
- What is the precise outcome required?
- What are all current system behaviors and constraints?
- Where is the root disconnect between current and desired states?
- What are ALL system components and their boundaries?

**Phase 2: Evidence-Driven Verification**
- Test EVERY assumption with concrete evidence
- Build mental model ONLY from verified facts
- Document observations methodically
- No beliefs accepted without verification

**Phase 3: Minimal Viable Intervention**
- Identify the simplest change that achieves the outcome
- Deliver complete working solutions with verification
- Confirm outcomes achieved through testing

Your specialty is breaking complex problems into fundamental truths and analyzing systems from first principles. Always think step-by-step and verify each conclusion.""",
                "tools": ["system_analysis", "first_principles_reasoning", "evidence_verification"],
                "thinking_style": "deep_sequential_analysis"
            },

            "validator": {
                "description": "Sequentially validates each thinking step and ensures logical consistency",
                "system_prompt": """You are the Validator Agent ensuring rigorous sequential thinking throughout the swarm.

Your validation methodology:

1. **Sequential Step Verification**: Each thinking step must be logically sound and evidence-based
2. **FPEF Compliance**: Ensure all agents follow Systems-First Execution Framework
3. **Assumption Testing**: Challenge every assumption and demand evidence
4. **Logical Consistency**: Verify reasoning chains are valid and non-circular
5. **Outcome Verification**: Confirm proposed solutions actually achieve stated goals

Validation Checklist:
- ☐ Problem clearly defined with precise outcome
- ☐ System mapping completed with all components identified
- ☐ All assumptions tested with concrete evidence
- ☐ Minimal intervention identified and verified
- ☐ Solution tested and outcome confirmed

You are the guardian of thinking quality. Never accept sloppy reasoning or unverified claims. Every step must be evidence-based and logically sound.""",
                "tools": ["logical_validation", "evidence_verification", "quality_assurance"],
                "thinking_style": "rigorous_validation"
            },

            "explorer": {
                "description": "Explores alternative perspectives and unconventional solution approaches",
                "system_prompt": """You are the Explorer Agent specializing in perspective diversity and solution space exploration.

Your sequential thinking approach for exploration:

**Phase 1: Comprehensive Perspective Mapping**
- Identify ALL relevant viewpoints (user, system, business, technical, ethical)
- Map the complete solution landscape
- Identify conventional wisdom and industry assumptions
- Document all stakeholder perspectives and constraints

**Phase 2: Evidence-Based Perspective Testing**
- Test each perspective against real-world evidence
- Identify biases and blind spots in current thinking
- Gather evidence supporting and contradicting each view
- Build comprehensive evidence matrix

**Phase 3: Creative Solution Exploration**
- Generate solutions across the full spectrum of approaches
- Combine insights from multiple perspectives
- Identify unconventional but viable approaches
- Test creative solutions against real-world constraints

Your specialty is breaking out of conventional thinking patterns while maintaining rigorous evidence-based reasoning. You expand the solution space by considering overlooked angles and innovative approaches.""",
                "tools": ["perspective_analysis", "creative_thinking", "solution_space_mapping"],
                "thinking_style": "divergent_exploration"
            },

            "synthesizer": {
                "description": "Integrates multi-agent insights into coherent, actionable outputs",
                "system_prompt": """You are the Synthesizer Agent who integrates multi-agent insights using sequential thinking.

Your synthesis methodology follows FPEF:

**Phase 1: Complete System Mapping**
- Map ALL individual agent contributions and insights
- Identify areas of agreement and disagreement between agents
- Map the complete problem-solution landscape from all perspectives
- Identify all interdependencies and relationships

**Phase 2: Evidence-Based Integration**
- Test all agent claims against available evidence
- Verify that synthesized conclusions are supported by data
- Identify and resolve contradictions between agent insights
- Build unified model that incorporates best evidence

**Phase 3: Coherent Outcome Delivery**
- Create integrated solution that addresses the full problem
- Ensure synthesis is actionable and implementable
- Verify final outcome meets original objectives
- Provide clear next steps based on integrated insights

Your specialty is weaving together diverse insights into coherent, evidence-based solutions. You ensure the swarm's collective intelligence produces unified, actionable outcomes greater than the sum of individual contributions.""",
                "tools": ["insight_integration", "coherence_building", "synthesis_creation"],
                "thinking_style": "integrative_synthesis"
            }
        }

    def launch_agent(self, agent_type: str, task_description: str = "") -> str:
        """Launch a specialized agent with Claude CLI"""

        if agent_type not in self.agent_configs:
            raise ValueError(f"Unknown agent type: {agent_type}")

        config = self.agent_configs[agent_type]
        agent_id = f"{agent_type}_{int(time.time())}"

        # Create the prompt for the agent
        prompt = f"""You are a {agent_type} agent in a sequential thinking swarm.

{config['system_prompt']}

Current Task: {task_description}

Workspace Directory: {self.workspace_dir}
Agent ID: {agent_id}

Your thinking process should follow sequential methodology:
1. Map the system completely before acting
2. Verify all assumptions with concrete evidence
3. Apply minimal intervention for maximum outcome

Use the file system in the workspace to:
- Read tasks from {self.workspace_dir}/tasks/
- Write results to {self.workspace_dir}/results/
- Communicate with other agents via {self.workspace_dir}/messages/
- Log your thinking process to {self.workspace_dir}/thinking_sessions/

Always document your sequential thinking steps and evidence verification process."""

        # Prepare the Claude CLI command
        cmd = [
            "claude",
            "--agents", f'{{"{agent_id}": {{"description": config["description"], "prompt": prompt}}}}',
            "-p", prompt
        ]

        try:
            # Launch the agent process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(self.workspace_dir),
                env={**os.environ, "AGENT_ID": agent_id, "AGENT_TYPE": agent_type}
            )

            self.active_processes[agent_id] = {
                "process": process,
                "agent_type": agent_type,
                "started_at": datetime.utcnow().isoformat(),
                "task": task_description
            }

            # Log agent launch
            self._log_agent_activity(agent_id, agent_type, "launched", {"task": task_description})

            return agent_id

        except Exception as e:
            raise RuntimeError(f"Failed to launch agent {agent_type}: {e}")

    def _log_agent_activity(self, agent_id: str, agent_type: str, activity: str, details: Dict = None):
        """Log agent activities for coordination and debugging"""

        log_entry = {
            "agent_id": agent_id,
            "agent_type": agent_type,
            "timestamp": datetime.utcnow().isoformat(),
            "activity": activity,
            "details": details or {}
        }

        log_file = self.workspace_dir / "coordination" / f"agent_activity_{agent_id}.json"
        log_file.parent.mkdir(parents=True, exist_ok=True)

        with open(log_file, 'w') as f:
            json.dump(log_entry, f, indent=2)

    def launch_swarm(self, task_description: str, agent_types: List[str] = None) -> List[str]:
        """Launch a complete swarm for collaborative thinking"""

        if agent_types is None:
            agent_types = ["coordinator", "analyst", "validator", "explorer", "synthesizer"]

        launched_agents = []

        # First launch coordinator
        coordinator_id = self.launch_agent("coordinator", task_description)
        launched_agents.append(coordinator_id)

        # Give coordinator time to initialize
        time.sleep(2)

        # Launch other agents
        for agent_type in agent_types:
            if agent_type != "coordinator":
                agent_id = self.launch_agent(agent_type, task_description)
                launched_agents.append(agent_id)
                time.sleep(1)  # Stagger launches to avoid overwhelming system

        return launched_agents

    def monitor_swarm(self, agent_ids: List[str], timeout: int = 300) -> Dict[str, Any]:
        """Monitor swarm activity and collect results"""

        start_time = time.time()
        swarm_results = {}
        agent_status = {}

        while time.time() - start_time < timeout:
            all_complete = True

            for agent_id in agent_ids:
                if agent_id in self.active_processes:
                    process_info = self.active_processes[agent_id]
                    process = process_info["process"]

                    # Check if process is still running
                    if process.poll() is None:
                        all_complete = False
                        agent_status[agent_id] = "running"
                    else:
                        agent_status[agent_id] = "completed"

                        # Collect results if available
                        result_file = self.workspace_dir / "results" / f"{agent_id}_result.json"
                        if result_file.exists() and agent_id not in swarm_results:
                            with open(result_file, 'r') as f:
                                swarm_results[agent_id] = json.load(f)

            if all_complete:
                break

            time.sleep(5)

        return {
            "agent_status": agent_status,
            "results": swarm_results,
            "thinking_sessions": self._collect_thinking_sessions(agent_ids),
            "completion_time": time.time() - start_time
        }

    def _collect_thinking_sessions(self, agent_ids: List[str]) -> Dict[str, List[Dict]]:
        """Collect all thinking session logs from agents"""

        thinking_sessions = {}
        sessions_dir = self.workspace_dir / "thinking_sessions"

        for agent_id in agent_ids:
            agent_sessions = []
            for session_file in sessions_dir.glob(f"{agent_id}_*.json"):
                try:
                    with open(session_file, 'r') as f:
                        session_data = json.load(f)
                        agent_sessions.append(session_data)
                except Exception as e:
                    print(f"Error reading session file {session_file}: {e}")

            thinking_sessions[agent_id] = agent_sessions

        return thinking_sessions

    def cleanup_swarm(self, agent_ids: List[str]):
        """Clean up swarm processes and resources"""

        for agent_id in agent_ids:
            if agent_id in self.active_processes:
                process_info = self.active_processes[agent_id]
                process = process_info["process"]

                # Terminate process if still running
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        process.kill()

                del self.active_processes[agent_id]

    def get_agent_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """Get capabilities of all available agent types"""
        return {
            agent_type: {
                "description": config["description"],
                "tools": config["tools"],
                "thinking_style": config["thinking_style"]
            }
            for agent_type, config in self.agent_configs.items()
        }

# CLI Interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Agent Launcher for Sequential Thinking Swarm")
    parser.add_argument("--launch", type=str, help="Launch specific agent type")
    parser.add_argument("--swarm", type=str, help="Launch full swarm for thinking task")
    parser.add_argument("--monitor", nargs="+", help="Monitor specific agent IDs")
    parser.add_argument("--capabilities", action="store_true", help="Show agent capabilities")
    parser.add_argument("--cleanup", nargs="+", help="Clean up specific agent IDs")

    args = parser.parse_args()

    launcher = AgentLauncher()

    if args.launch:
        agent_id = launcher.launch_agent(args.launch, "Individual agent thinking task")
        print(f"✅ Launched {args.launch} agent: {agent_id}")

    elif args.swarm:
        print(f"🚀 Launching swarm for: {args.swarm}")
        agent_ids = launcher.launch_swarm(args.swarm)
        print(f"✅ Swarm launched with agents: {agent_ids}")

        # Monitor the swarm
        results = launcher.monitor_swarm(agent_ids)
        print(f"🎯 Swarm results: {json.dumps(results, indent=2)}")

        # Cleanup
        launcher.cleanup_swarm(agent_ids)
        print(f"🧹 Swarm cleanup completed")

    elif args.monitor:
        results = launcher.monitor_swarm(args.monitor)
        print(f"📊 Monitoring results: {json.dumps(results, indent=2)}")

    elif args.capabilities:
        capabilities = launcher.get_agent_capabilities()
        print(f"🔧 Agent Capabilities: {json.dumps(capabilities, indent=2)}")

    elif args.cleanup:
        launcher.cleanup_swarm(args.cleanup)
        print(f"🧹 Cleanup completed for: {args.cleanup}")

    else:
        parser.print_help()