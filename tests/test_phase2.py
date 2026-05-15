import sys
import os
import json
from unittest.mock import MagicMock

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.crud.trace_logger import TraceLogger

def test_trace_logging():
    log_file = "traces/test_traces.jsonl"
    if os.path.exists(log_file):
        os.remove(log_file)
        
    logger = TraceLogger(log_file=log_file)
    
    # Mock GameState
    game_state = MagicMock()
    game_state.session_metadata.tick_id = 42
    game_state.player.health = 100
    game_state.player.active_element = "Fire"
    
    # Mock HiveTactics
    tactics = MagicMock()
    tactics.hive_tactic = "Aggressive"
    tactics.arbiter_check = "PASSED"
    tactics.agentic_negotiation.model_dump.return_value = {
        "pharaoh_proposal": "Attack",
        "arbiter_veto": "None",
        "empathy_note": "Keep it cool",
        "final_consensus": "Attack now"
    }
    
    # Log trace
    logger.log_trace(game_state, tactics)
    
    # Verify file exists
    assert os.path.exists(log_file)
    
    # Verify content
    with open(log_file, "r") as f:
        line = f.readline()
        entry = json.loads(line)
        
        assert entry["tick_id"] == 42
        assert entry["player health"] == 100
        assert entry["active element"] == "Fire"
        assert entry["hive_tactic"] == "Aggressive"
        assert entry["arbiter_check"] == "PASSED"
        assert entry["agentic_negotiation"]["pharaoh_proposal"] == "Attack"
    
    # Test retrieval
    recent = logger.get_recent_traces(limit=1)
    assert len(recent) == 1
    assert recent[0]["tick_id"] == 42
    
    print("Test Trace Logging: PASSED")
    
    # Cleanup
    if os.path.exists(log_file):
        os.remove(log_file)

if __name__ == "__main__":
    try:
        test_trace_logging()
    except Exception as e:
        print(f"Test Failed: {e}")
        sys.exit(1)
