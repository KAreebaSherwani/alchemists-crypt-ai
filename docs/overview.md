# The Alchemist's Crypt - AI Backend Overview

## Project Mission
To provide a reactive, tactical, and immersive AI "Hive Mind" for a mobile FPS. The AI doesn't just play to win; it plays to maintain a "Flow State" for the player, balancing challenge with mercy through a unique agentic negotiation system.

## Architecture
- **Framework**: FastAPI
- **AI Core**: Gemini 1.5 Flash
- **Logic Pattern**: The Council of Three (Pharaoh, Arbiter, Empathy)
- **Integration**: Unity calls the API every 2 seconds via JSON.

## The Council of Three
1. **Pharaoh**: The strategist. Focused on aggressive maneuvers and player elimination.
2. **Arbiter**: The referee. Ensures plans are "fair" and physically possible within game rules.
3. **Empathy**: The balancer. Monitors player health and behavior to inject mercy or adjust intensity.
