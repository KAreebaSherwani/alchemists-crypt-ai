from pydantic import BaseModel, Field
from typing import List, Optional, Tuple

# --- Input Models (Unity to FastAPI) ---

class SessionMetadata(BaseModel):
    tick_id: int
    last_tactic_success: bool
    difficulty_scaling: float

class PlayerState(BaseModel):
    pos: List[float]  # [x, y, z]
    vel: List[float]  # [x, y, z]
    active_element: str
    health: int
    is_firing: bool

class MummyState(BaseModel):
    id: int
    pos: List[float]
    hp: int
    state: str

class GameState(BaseModel):
    gameState: str
    session_metadata: SessionMetadata
    player: PlayerState
    mummies: List[MummyState]
    pharaoh_active: Optional[bool] = False
    nearby_environment: Optional[str] = ""

# --- Output Models (FastAPI to Unity) ---

class AgenticNegotiation(BaseModel):
    pharaoh_proposal: str
    arbiter_veto: str
    empathy_note: str
    final_consensus: str

class MummyInstruction(BaseModel):
    id: int
    action: str
    target: List[float]
    delay: Optional[float] = 0.0
    speed_mult: Optional[float] = 1.0

class HiveTactics(BaseModel):
    hive_tactic: str
    agentic_negotiation: AgenticNegotiation
    reasoning_trace: str
    arbiter_check: str
    instructions: List[MummyInstruction]
    narration: str
