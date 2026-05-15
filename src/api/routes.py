from fastapi import APIRouter, Depends, HTTPException
from src.models.schemas import GameState, HiveTactics
from src.agents.council import HiveMindCouncil
from src.agents.baseline_agent import BaselineAgent
from src.crud.trace_logger import logger
from typing import List, Dict, Any

router = APIRouter()
council = HiveMindCouncil()
baseline_agent = BaselineAgent()

@router.post("/hive-mind", response_model=HiveTactics)
async def get_hive_mind_tactics(game_state: GameState):
    """
    Unity sends game state, AI Council returns tactical instructions.
    """
    try:
        tactics = await council.get_tactics(game_state)
        # Persistent logging for analytics and debugging
        logger.log_trace(game_state, tactics, mode="agentic")
        return tactics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/hive-mind/baseline", response_model=HiveTactics)
async def get_baseline_tactics(game_state: GameState):
    """
    Unity sends game state, Baseline Agent returns fixed rules.
    """
    try:
        tactics = baseline_agent.get_tactics(game_state)
        logger.log_trace(game_state, tactics, mode="baseline")
        return tactics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/traces", response_model=List[Dict[str, Any]])
async def get_traces():
    """
    Returns the last 10 trace entries for debugging.
    """
    return logger.get_recent_traces(limit=10)

@router.get("/traces/compare", response_model=Dict[str, Any])
async def get_comparison_stats():
    """
    Returns side-by-side stats for agentic vs baseline.
    """
    return logger.get_comparison_stats()


