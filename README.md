# 🏺 The Alchemist's Crypt — AI Hive Mind Backend

> *"The curse does not breathe, yet it feels your pulse."*

A tactical FPS mobile game where a **Council of Three AI agents** controls a tomb of mummies that adapt in real-time to the player's every move. Built for the **Agentic Game Quest — Challenge 4** using Google Antigravity 

---

## 🎮 The Game Hook — What Makes This Unputdownable

The player wields an **Alchemical Focus** with three elemental modes:

| Element | Effect | Hive Mind Counter-Response |
|---|---|---|
| 🔥 Sulfur | High AOE Fire Damage | Mummies **scatter** and keep distance |
| 💧 Mercury | Slows enemies | Hive Mind orders **ambush** formations |
| 💎 Salt | Stuns & Purifies | Mummies form **protective guards** around High-Priests |

Every choice teaches the AI. Every session is different. The player is never fighting the same enemy twice — they are fighting an enemy that has **studied them**.

---

## 🧠 The Agentic Core — Council of Three

The Hive Mind is not a single AI. It is three agents in constant negotiation:

```
PHARAOH  →  Proposes aggressive tactics based on player position & element
    ↓
ARBITER  →  Vetoes unfair/impossible plans (hard rule: no wipeout if health < 30)
    ↓
EMPATHY  →  Monitors player stress — injects mercy if frustration detected
    ↓
CONSENSUS → Only reached when Arbiter outputs APPROVED
```

This negotiation is **visible in real-time** through the Agent Trace HUD in-game, giving judges full transparency into the AI's decision-making process.

### Sample Agentic Negotiation Output

```json
{
  "hive_tactic": "Suppressive Flank",
  "agentic_negotiation": {
    "pharaoh_proposal": "Full aggressive rush to capitalize on low player health.",
    "arbiter_veto": "VETO: Player health (45) + Sulfur AOE suggests a rush is unfair. Re-calculating.",
    "empathy_note": "Player showing frustration patterns. Suggest 1.5s delay on Unit 1.",
    "final_consensus": "APPROVED: Flank maneuver with delay to maintain Flow State."
  },
  "reasoning_trace": "Pivoting from Rush to Flank. Countering Sulfur via staggered positioning.",
  "arbiter_check": "APPROVED. Intensity: 0.78 (Optimal).",
  "narration": "The fires of sulfur cannot cleanse this curse!"
}
```

---

## 🏗️ Architecture

```
Unity Mobile App (C#)
        │
        │  POST /api/v1/hive-mind  (every 2 seconds)
        │  GameState JSON →
        ↓
┌─────────────────────────────────────────┐
│         FastAPI Backend (Python)        │
│                                         │
│  routes.py → HiveMindCouncil            │
│                   │                     │
│              google.genai               │
│           Gemini Flash Model            │
│                   │                     │
│     Council of Three System Prompt      │
│   (Pharaoh + Arbiter + Empathy)         │
│                   │                     │
│  TraceLogger → agent_traces.jsonl       │
│                                         │
│  Deployed on Railway (24/7)             │
└─────────────────────────────────────────┘
        │
        │  ← HiveTactics JSON response
        ↓
Unity applies mummy movement instructions
Agent Trace HUD displays negotiation log
```

### Antigravity's Role
Google Antigravity served as the **primary orchestrator** throughout development:
- Generated the full OOP project structure and all modules
- Planned and executed each phase with explicit reasoning traces
- Managed the multi-agent Council prompt design and validation logic
- Produced all documentation artifacts as `.md` files per phase

---

## 🔌 API Reference

**Base URL:** `https://alchemists-crypt-ai-production.up.railway.app`

### POST `/api/v1/hive-mind`
Unity sends game state → Hive Mind Council returns tactics.

**Request:**
```json
{
  "gameState": "Chamber_02",
  "session_metadata": {
    "tick_id": 442,
    "last_tactic_success": false,
    "difficulty_scaling": 0.85
  },
  "player": {
    "pos": [12.4, 0.0, 5.2],
    "vel": [2.1, 0.0, -0.5],
    "active_element": "Sulfur",
    "health": 45,
    "is_firing": true
  },
  "mummies": [
    {"id": 1, "pos": [2.0, 0.0, 2.1], "hp": 50, "state": "Stunned"},
    {"id": 2, "pos": [5.5, 0.0, 8.3], "hp": 100, "state": "Chasing"}
  ]
}
```

### POST `/api/v1/hive-mind/baseline`
Same input → Fixed-rule "Standard Rush" response (for baseline comparison).

### GET `/api/v1/traces`
Returns last 10 AI decision traces with full negotiation logs.

### GET `/api/v1/traces/compare`
Returns side-by-side stats: agentic vs baseline tactical diversity.

---

## 📊 Baseline Comparison (+5% Bonus)

We implemented a `BaselineAgent` (Dumb AI) that always executes a fixed "Standard Rush" — all mummies chase the player with no adaptation.

| Metric | Baseline (Dumb AI) | Hive Mind (Agentic) |
|---|---|---|
| Unique tactics generated | 1 (always "Standard Rush") | 8+ per session |
| Element adaptation | ❌ None | ✅ Sulfur/Mercury/Salt counters |
| Player health consideration | ❌ None | ✅ Arbiter veto at health < 30 |
| Frustration prevention | ❌ None | ✅ Empathy mercy injection |
| Tactical variety | ❌ Predictable | ✅ Flank, Ambush, Scatter, Guard |

The `/api/v1/traces/compare` endpoint provides **live proof** of this difference during the demo.

---

## 🛡️ Robustness & Fallback

**Lifeboat Protocol:** If Gemini API is unavailable or times out, the system automatically returns a safe `"Standard Patrol"` fallback response so Unity never crashes or hangs.

**Edge cases handled:**
- API quota exhaustion → fallback tactics returned
- Malformed JSON from Gemini → caught, fallback triggered, error logged
- Missing API key → warning printed, fallback active
- All failures logged with full stack trace

---

## 💰 Cost & Scalability

| Metric | Value |
|---|---|
| Cost per API call | ~$0.000075 (Gemini Flash pricing) |
| Latency per call | ~800ms–1.2s average |
| Calls per game session (10 min) | ~300 (every 2 seconds) |
| Cost per 10-min session | ~$0.022 |
| 100x scale (100 concurrent players) | ~$2.20 per 10 minutes |

Railway free tier handles ~100 concurrent requests. For 10x/100x scaling: add Railway Pro + Redis caching for repeated game states.

---

## 🗂️ Data Schemas

All schemas defined in `src/models/schemas.py` using Pydantic V2.

**GameState** (Unity → API): `gameState`, `session_metadata`, `player`, `mummies[]`

**HiveTactics** (API → Unity): `hive_tactic`, `agentic_negotiation`, `reasoning_trace`, `arbiter_check`, `instructions[]`, `narration`

**TraceEntry** (logged to JSONL): `timestamp`, `mode`, `tick_id`, `player_health`, `active_element`, `hive_tactic`, `arbiter_check`, `agentic_negotiation`

---

## ⚙️ Setup (Local Development)

```bash
git clone https://github.com/YOURUSERNAME/alchemists-crypt-ai
cd alchemists-crypt-ai
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
echo GEMINI_API_KEY=your_key > .env
python main.py
# Visit http://localhost:8000/docs
```

---

## 🧪 Running Tests

```bash
.venv\Scripts\python.exe -m pytest tests/ -v
```

Expected: 4 test files, all passing.

---

## 📁 Project Structure

```
alchemists-crypt-ai/
├── phases/           # Phase-by-phase build logs (Antigravity artifacts)
│   ├── phase1.md
│   ├── phase2.md
│   └── phase3.md
├── docs/             # Architecture docs and system prompts
│   ├── overview.md
│   └── council_system_prompt.md
├── src/
│   ├── agents/
│   │   ├── council.py          # HiveMindCouncil (Gemini Flash)
│   │   └── baseline_agent.py   # BaselineAgent (fixed rules)
│   ├── api/
│   │   └── routes.py           # FastAPI endpoints
│   ├── crud/
│   │   └── trace_logger.py     # JSONL trace persistence
│   └── models/
│       └── schemas.py          # Pydantic V2 schemas
├── tests/
│   ├── test_hive_mind.py
│   ├── test_phase2.py
│   └── test_phase3.py
├── traces/
│   └── agent_traces.jsonl      # Live AI decision log
├── main.py
├── requirements.txt
└── Procfile                    # Railway deployment
```

---

## ⚠️ Limitations

- Gemini free tier has rate limits; production deployment should use a paid key
- `agent_traces.jsonl` is file-based; replace with PostgreSQL for production scale
- Unity integration requires same-network or public URL access (Railway handles this)
- Mummy pathfinding logic lives in Unity (NavMesh); backend provides targets only

---

## 🔒 Privacy Note

No personal data is stored. Trace logs contain only game state metrics (positions, health values, element choices). No player identity, device data, or biometrics are collected or transmitted.

---

*Built with Google Antigravity | Challenge 4: Agentic Game Quest*
