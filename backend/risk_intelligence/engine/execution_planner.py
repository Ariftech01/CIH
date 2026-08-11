from typing import List, Dict, Any

class ExecutionPlanner:
    """
    Execution Planner for CRIE.
    Determines analysis mode (FULL, PARTIAL, INCREMENTAL), execution sequence,
    and required component scope based on request parameters.
    """

    def plan_execution(self, analysis_type: str = "FULL", scope: List[str] = None) -> Dict[str, Any]:
        valid_agents = ["Site Risk Agent", "Safety Agent", "Compliance Agent", "Insurance Agent", "Reporting Agent"]

        if analysis_type == "FULL" or not scope:
            target_agents = valid_agents
            mode = "FULL"
        elif analysis_type == "PARTIAL":
            target_agents = [a for a in valid_agents if any(s.lower() in a.lower() for s in scope)]
            if not target_agents:
                target_agents = valid_agents
            mode = "PARTIAL"
        elif analysis_type == "INCREMENTAL":
            target_agents = [a for a in valid_agents if any(s.lower() in a.lower() for s in scope)]
            if not target_agents:
                target_agents = ["Site Risk Agent", "Safety Agent"]
            mode = "INCREMENTAL"
        else:
            target_agents = valid_agents
            mode = "FULL"

        return {
            "analysis_type": analysis_type,
            "mode": mode,
            "target_agents": target_agents,
            "execution_sequence": target_agents,
            "estimated_stages": len(target_agents) + 3
        }

execution_planner = ExecutionPlanner()
