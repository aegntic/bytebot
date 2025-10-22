#!/usr/bin/env python3
"""
Sequential Thinking & Ultrathink Swarm Demonstration

Demonstrates the capabilities of the multi-agent swarm system
where each agent uses sequential thinking individually while the
swarm performs collaborative ultrathink.
"""

import json
import time
from datetime import datetime
from swarm_orchestrator import SwarmOrchestrator
from agent_launcher import AgentLauncher

class SwarmDemo:
    """Demonstrates sequential thinking and ultrathink capabilities"""

    def __init__(self):
        self.orchestrator = SwarmOrchestrator(max_agents=5)
        self.launcher = AgentLauncher()

    def demo_agent_capabilities(self):
        """Show the specialized capabilities of each agent type"""
        print("🤖 Sequential Thinking & Ultrathink Agent Swarm Capabilities")
        print("=" * 60)

        capabilities = self.launcher.get_agent_capabilities()

        for agent_type, config in capabilities.items():
            print(f"\n🧠 {agent_type.upper()} AGENT")
            print(f"   Description: {config['description']}")
            print(f"   Tools: {', '.join(config['tools'])}")
            print(f"   Thinking Style: {config['thinking_style']}")

    def demo_sequential_thinking_individual(self, problem: str):
        """Demonstrate individual agent sequential thinking"""
        print(f"\n🔄 INDIVIDUAL SEQUENTIAL THINKING DEMO")
        print(f"Problem: {problem}")
        print("=" * 50)

        # Initialize swarm
        swarm_result = self.orchestrator.initialize_swarm()
        print(f"✅ Swarm initialized: {len(swarm_result['agents'])} agents ready")

        # Launch individual agents for sequential thinking
        print("\n📝 Launching agents for sequential thinking...")

        agent_tasks = [
            ("analyst", f"Analyze this problem using sequential thinking: {problem}"),
            ("validator", f"Validate the sequential thinking approach for: {problem}"),
            ("explorer", f"Explore solution spaces using sequential thinking for: {problem}")
        ]

        launched_agents = []
        for agent_type, task in agent_tasks:
            try:
                agent_id = self.launcher.launch_agent(agent_type, task)
                launched_agents.append(agent_id)
                print(f"✅ Launched {agent_type}: {agent_id}")
            except Exception as e:
                print(f"❌ Failed to launch {agent_type}: {e}")

        if launched_agents:
            print(f"\n⏱️ Monitoring {len(launched_agents)} agents...")
            results = self.launcher.monitor_swarm(launched_agents, timeout=60)

            print("\n📊 Sequential Thinking Results:")
            for agent_id, status in results['agent_status'].items():
                print(f"   {agent_id}: {status}")

            print("\n🧠 Thinking Sessions Collected:")
            for agent_id, sessions in results['thinking_sessions'].items():
                if sessions:
                    print(f"   {agent_id}: {len(sessions)} thinking sessions")
                    for session in sessions:
                        print(f"     - {session.get('stage', 'unknown')}: {session.get('timestamp', '')}")

            # Cleanup
            self.launcher.cleanup_swarm(launched_agents)
            print("\n🧹 Individual agents cleaned up")

    def demo_collaborative_ultrathink(self, problem: str):
        """Demonstrate collaborative ultrathink with full swarm"""
        print(f"\n🌟 COLLABORATIVE ULTRATHINK DEMO")
        print(f"Problem: {problem}")
        print("=" * 50)

        # Execute full swarm ultrathink
        print("🚀 Starting collaborative ultrathink session...")
        start_time = time.time()

        try:
            result = self.orchestrator.execute_sequential_swarm_thinking(problem)

            end_time = time.time()
            duration = end_time - start_time

            print(f"✅ Ultrathink completed in {duration:.2f} seconds")
            print(f"\n🎯 SWARM ULTRATHINK RESULTS:")
            print(f"   Individual Sequential Analysis: {len(result.get('individual_sequential_thinking', {}))} agents")
            print(f"   Collaborative Ultrathink: {len(result.get('collaborative_ultrathink', {}))} agents")
            print(f"   Final Synthesis: {'✅' if result.get('final_synthesis') else '❌'}")
            print(f"   Swarm Consensus: {result.get('swarm_consensus', {}).get('consensus_level', 'unknown')}")

            # Show detailed breakdown
            if 'individual_sequential_thinking' in result:
                print(f"\n📝 INDIVIDUAL SEQUENTIAL THINKING BREAKDOWN:")
                for agent_id, thinking in result['individual_sequential_thinking'].items():
                    print(f"   {agent_id}:")
                    for phase, content in thinking.items():
                        print(f"     {phase}: ✅")

            if 'collaborative_ultrathink' in result:
                print(f"\n🧠 COLLABORATIVE ULTRATHINK BREAKDOWN:")
                for agent_id, ultrathink in result['collaborative_ultrathink'].items():
                    print(f"   {agent_id}:")
                    for phase, content in ultrathink.items():
                        print(f"     {phase}: ✅")

        except Exception as e:
            print(f"❌ Ultrathink failed: {e}")

    def demo_sequential_vs_ultrathink(self, problem: str):
        """Compare individual sequential thinking vs collaborative ultrathink"""
        print(f"\n🔄 COMPARISON: Sequential vs Ultrathink")
        print(f"Problem: {problem}")
        print("=" * 50)

        # Individual sequential thinking
        print("\n1️⃣ INDIVIDUAL SEQUENTIAL THINKING")
        start_time = time.time()

        self.demo_sequential_thinking_individual(problem)

        sequential_time = time.time() - start_time

        # Collaborative ultrathink
        print("\n2️⃣ COLLABORATIVE ULTRATHINK")
        start_time = time.time()

        self.demo_collaborative_ultrathink(problem)

        ultrathink_time = time.time() - start_time

        # Comparison
        print(f"\n📊 COMPARISON RESULTS:")
        print(f"   Individual Sequential Thinking: {sequential_time:.2f} seconds")
        print(f"   Collaborative Ultrathink: {ultrathink_time:.2f} seconds")
        print(f"   Ultrathink Multiplier: {ultrathink_time/sequential_time:.2f}x")
        print(f"   Quality Improvement: Collaborative insights + synthesis")

    def demo_complex_problem_solving(self):
        """Demonstrate swarm solving a complex multi-dimensional problem"""
        complex_problem = """
        Design an AI-powered education platform that adapts to individual learning styles while:
        1. Ensuring privacy and data security
        2. Maintaining human teacher oversight
        3. Being accessible to diverse socioeconomic backgrounds
        4. Incorporating ethical AI considerations
        5. Scaling to millions of users efficiently

        Consider technical, pedagogical, ethical, and business dimensions.
        """

        print(f"🎯 COMPLEX PROBLEM SOLVING DEMO")
        print(f"Using full sequential thinking + collaborative ultrathink approach...")
        print("=" * 70)

        self.demo_collaborative_ultrathink(complex_problem)

    def interactive_demo(self):
        """Interactive demonstration where user can input problems"""
        print("🎮 INTERACTIVE SEQUENTIAL THINKING & ULTRATHINK DEMO")
        print("=" * 50)

        while True:
            print("\n📝 Choose demo type:")
            print("1. Show agent capabilities")
            print("2. Individual sequential thinking")
            print("3. Collaborative ultrathink")
            print("4. Sequential vs Ultrathink comparison")
            print("5. Complex problem solving")
            print("6. Exit")

            choice = input("\nEnter choice (1-6): ").strip()

            if choice == "1":
                self.demo_agent_capabilities()
            elif choice == "2":
                problem = input("Enter problem for sequential thinking: ").strip()
                if problem:
                    self.demo_sequential_thinking_individual(problem)
            elif choice == "3":
                problem = input("Enter problem for collaborative ultrathink: ").strip()
                if problem:
                    self.demo_collaborative_ultrathink(problem)
            elif choice == "4":
                problem = input("Enter problem for comparison: ").strip()
                if problem:
                    self.demo_sequential_vs_ultrathink(problem)
            elif choice == "5":
                self.demo_complex_problem_solving()
            elif choice == "6":
                print("👋 Thanks for trying the Sequential Thinking & Ultrathink Swarm!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-6.")

# CLI Interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sequential Thinking & Ultrathink Swarm Demo")
    parser.add_argument("--capabilities", action="store_true", help="Show agent capabilities")
    parser.add_argument("--sequential", type=str, help="Run individual sequential thinking on problem")
    parser.add_argument("--ultrathink", type=str, help="Run collaborative ultrathink on problem")
    parser.add_argument("--compare", type=str, help="Compare sequential vs ultrathink on problem")
    parser.add_argument("--complex", action="store_true", help="Run complex problem solving demo")
    parser.add_argument("--interactive", action="store_true", help="Run interactive demo")

    args = parser.parse_args()

    demo = SwarmDemo()

    if args.capabilities:
        demo.demo_agent_capabilities()
    elif args.sequential:
        demo.demo_sequential_thinking_individual(args.sequential)
    elif args.ultrathink:
        demo.demo_collaborative_ultrathink(args.ultrathink)
    elif args.compare:
        demo.demo_sequential_vs_ultrathink(args.compare)
    elif args.complex:
        demo.demo_complex_problem_solving()
    elif args.interactive:
        demo.interactive_demo()
    else:
        # Run full demo by default
        print("🚀 Starting Sequential Thinking & Ultrathink Swarm Demo")
        demo.demo_agent_capabilities()

        demo_problem = "How might we design more efficient renewable energy storage systems?"
        demo.demo_sequential_vs_ultrathink(demo_problem)

        print("\n" + "="*60)
        print("✅ Demo completed! Try --interactive for hands-on experience.")
        print("🤖 Each agent uses sequential thinking (FPEF) individually")
        print("🧠 The swarm performs ultrathink through collaboration")