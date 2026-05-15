from src.models.schemas import GameState, HiveTactics, AgenticNegotiation, MummyInstruction

class BaselineAgent:
    """
    Fixed-rule agent for baseline comparison against the Hive Mind.
    Does not use AI or external calls.
    """
    def get_tactics(self, game_state: GameState) -> HiveTactics:
        # Fixed mummies behavior
        instructions = [
            MummyInstruction(
                id=m.id,
                action="chase",
                target=game_state.player.pos,
                delay=0.0,
                speed_mult=1.0
            ) for m in game_state.mummies
        ]
        
        return HiveTactics(
            hive_tactic="Standard Rush",
            agentic_negotiation=AgenticNegotiation(
                pharaoh_proposal="Rush the player.",
                arbiter_veto="None",
                empathy_note="None",
                final_consensus="Execute rush."
            ),
            reasoning_trace="Fixed rule: always rush.",
            arbiter_check="APPROVED",
            instructions=instructions,
            narration="The dead know only one path forward."
        )
