import sys
import os
import json
from unittest.mock import MagicMock

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agents.baseline_agent import BaselineAgent
from src.crud.trace_logger import TraceLogger
from src.models.schemas import GameState, SessionMetadata, PlayerState, MummyState

def test_baseline_logic():
    agent = BaselineAgent()
    
    # Create real GameState object for testing
    game_state = GameState(
        gameState="active",
        session_metadata=SessionMetadata(tick_id=1, last_tactic_success=True, difficulty_scaling=1.0),
        player=PlayerState(pos=[0,0,0], vel=[0,0,0], active_element="Fire", health=100, is_firing=False),
        mummies=[MummyState(id=1, pos=[10,0,10], hp=50, state="idle")]
    )
    
    tactics = agent.get_tactics(game_state)
    
    assert tactics.hive_tactic == "Standard Rush"
    assert tactics.instructions[0].action == "chase"
    assert tactics.agentic_negotiation.final_consensus == "Execute rush."
    print("Baseline Logic: PASSED")

def test_comparison_stats():
    log_file = "traces/test_compare.jsonl"
    if os.path.exists(log_file):
        os.remove(log_file)
        
    logger = TraceLogger(log_file=log_file)
    
    # Mock data
    game_state = MagicMock()
    game_state.session_metadata.tick_id = 1
    game_state.player.health = 100
    game_state.player.active_element = "Fire"
    
    tactics_a = MagicMock()
    tactics_a.hive_tactic = "Agentic Tactic"
    tactics_a.arbiter_check = "APPROVED"
    tactics_a.agentic_negotiation.model_dump.return_value = {}
    
    tactics_b = MagicMock()
    tactics_b.hive_tactic = "Standard Rush"
    tactics_b.arbiter_check = "APPROVED"
    tactics_b.agentic_negotiation.model_dump.return_value = {}
    
    # Log some traces
    logger.log_trace(game_state, tactics_a, mode="agentic")
    logger.log_trace(game_state, tactics_a, mode="agentic")
    logger.log_trace(game_state, tactics_b, mode="baseline")
    
    stats = logger.get_comparison_stats()
    
    assert stats["total_agentic"] == 2
    assert stats["total_baseline"] == 1
    assert "Agentic Tactic" in stats["agentic_unique_tactics"]
    assert "Standard Rush" in stats["baseline_unique_tactics"]
    
    print("Comparison Stats: PASSED")
    
    if os.path.exists(log_file):
        os.remove(log_file)

if __name__ == "__main__":
    try:
        test_baseline_logic()
        test_comparison_stats()
    except Exception as e:
        print(f"Test Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
