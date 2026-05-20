import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from src.models.schemas import GameState, HiveTactics

load_dotenv()

class HiveMindCouncil:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            # Fallback for testing/demonstration if no key is set yet
            print("WARNING: GEMINI_API_KEY not found in environment.")
        
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-3.1-flash-lite"
        
        self.system_prompt = (
            "You are the Alchemist's Crypt Hive-Mind Council. Output MUST be valid JSON only — no markdown, no preamble, no explanation. "
            "You have three distinct personas who MUST debate before reaching consensus: PHARAOH proposes aggressive tactics based on player position and element choice. "
            "ARBITER vetoes any plan that is physically impossible, uses invalid coordinates, or risks a player wipe when health is below 30 — if vetoed, Pharaoh must re-propose. "
            "EMPATHY monitors player stress: if health is below 25 or the same tactic failed last tick, inject a mercy delay or alchemical drop. "
            "Consensus is ONLY reached when Arbiter explicitly outputs APPROVED. The agentic_negotiation field MUST show the full internal debate including any vetoes and re-proposals. "
            "Adapt mummy tactics based on active_element: Sulfur=scatter/distance, Mercury=ambush counters, Salt=protective guards around High-Priests. "
            "Return only a valid JSON object with these keys: hive_tactic, agentic_negotiation (object with pharaoh_proposal, arbiter_veto, empathy_note, final_consensus), "
            "reasoning_trace, arbiter_check, instructions (array of objects with id, action, target, delay, speed_mult), narration."
        )

    async def get_tactics(self, game_state: GameState) -> HiveTactics:
        # Prepare game state as JSON string for the prompt
        state_json = game_state.model_dump_json()
        
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_id,
                contents=state_json,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt
                )
            )
            
            # Extract JSON from response (handling potential markdown formatting from AI)
            text = response.text.strip()
            if text.startswith("```json"):
                text = text.replace("```json", "", 1).replace("```", "", 1).strip()
            elif text.startswith("```"):
                text = text.replace("```", "", 2).strip()
            
            tactics_dict = json.loads(text)
            return HiveTactics(**tactics_dict)
            
        except Exception as e:
            print(f"Error calling Gemini or parsing response: {e}")
            # Return a fallback tactic in case of failure
            return self._get_fallback_tactics(game_state)

    def _get_fallback_tactics(self, game_state: GameState) -> HiveTactics:
        """
        Called when Gemini API is unavailable (quota exceeded, invalid key, etc).
        Returns a useful fallback: mummies chase/flank the player instead of idling.
        NOTE: GEMINI_API_KEY appears to be revoked. Update the key on Railway to restore AI.
        """
        player_pos = game_state.player.pos  # [x, y, z]
        instructions = []
        for m in game_state.mummies:
            # Alternate: half chase directly, half try to flank (offset left/right)
            if m.id % 2 == 0:
                # Even IDs: flank left (+15 on X)
                target = [player_pos[0] + 15.0, player_pos[1], player_pos[2]]
                action = "flank"
            else:
                # Odd IDs: chase directly toward player
                target = player_pos
                action = "chase"
            instructions.append({
                "id": m.id,
                "action": action,
                "target": target,
                "delay": 0.0,
                "speed_mult": 1.2
            })

        return HiveTactics(
            hive_tactic="Autonomous Patrol",
            agentic_negotiation={
                "pharaoh_proposal": "Chase and flank the intruder.",
                "arbiter_veto": "None",
                "empathy_note": "AI backend offline — using autonomous rules.",
                "final_consensus": "Execute chase/flank pattern."
            },
            reasoning_trace="[FALLBACK] Gemini API unavailable. API key may be revoked or quota exceeded. Update GEMINI_API_KEY on Railway. Mummies executing autonomous chase/flank.",
            arbiter_check="APPROVED",
            instructions=instructions,
            narration="The ancient dead need no orders... they hunger."
        )

