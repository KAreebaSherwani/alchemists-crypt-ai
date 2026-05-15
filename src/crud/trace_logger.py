import json
import os
from datetime import datetime
from typing import List, Dict, Any

class TraceLogger:
    """
    Utility class to log AI reasoning traces for debugging and analytics.
    Saves traces to a .jsonl file.
    """
    def __init__(self, log_file: str = "traces/agent_traces.jsonl"):
        self.log_file = log_file
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def log_trace(self, game_state: Any, tactics: Any, mode: str = "agentic"):
        """
        Logs a single trace entry with game state, AI decision details, and mode.
        """
        timestamp = datetime.now().isoformat()
        
        # Construct the log entry from Pydantic models
        entry = {
            "timestamp": timestamp,
            "mode": mode,
            "tick_id": game_state.session_metadata.tick_id,
            "player health": game_state.player.health,
            "active element": game_state.player.active_element,
            "hive_tactic": tactics.hive_tactic,
            "arbiter_check": tactics.arbiter_check,
            "agentic_negotiation": tactics.agentic_negotiation.model_dump()
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def get_recent_traces(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Returns the last 'limit' trace entries.
        """
        if not os.path.exists(self.log_file):
            return []
        
        traces = []
        try:
            with open(self.log_file, "r") as f:
                for line in f:
                    if line.strip():
                        traces.append(json.loads(line))
        except Exception as e:
            print(f"Error reading trace logs: {e}")
            return []
            
        return traces[-limit:]

    def get_comparison_stats(self) -> Dict[str, Any]:
        """
        Returns side-by-side stats for agentic vs baseline performance.
        """
        if not os.path.exists(self.log_file):
            return {
                "total_agentic": 0,
                "total_baseline": 0,
                "agentic_unique_tactics": [],
                "baseline_unique_tactics": []
            }
            
        agentic_count = 0
        baseline_count = 0
        agentic_tactics = set()
        baseline_tactics = set()
        
        try:
            with open(self.log_file, "r") as f:
                for line in f:
                    if line.strip():
                        entry = json.loads(line)
                        mode = entry.get("mode", "agentic")
                        tactic = entry.get("hive_tactic")
                        
                        if mode == "agentic":
                            agentic_count += 1
                            if tactic: agentic_tactics.add(tactic)
                        else:
                            baseline_count += 1
                            if tactic: baseline_tactics.add(tactic)
        except Exception as e:
            print(f"Error computing stats: {e}")
            
        return {
            "total_agentic": agentic_count,
            "total_baseline": baseline_count,
            "agentic_unique_tactics": sorted(list(agentic_tactics)),
            "baseline_unique_tactics": sorted(list(baseline_tactics))
        }


# Singleton instance for app-wide use
logger = TraceLogger()

