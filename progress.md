# Project 2 — MFT Operations Agent: Progress Tracker

## Goal
Build an AI-powered chat agent for MFT operations support engineers.
Deploy on Hugging Face Spaces by end of Day 5.

---

## Status: Day 4 Complete ✅ — Live on Hugging Face Spaces

🔗 https://huggingface.co/spaces/aditya1401/mft-operations-agent

---

## Day Plan

| Day | Goal | Status |
|-----|------|--------|
| Day 1 | FastAPI + LangGraph agent + chat UI working locally | ✅ Done |
| Day 2 | Tools reading from docs, ChromaDB vector search, tools stabilized | ✅ Done |
| Day 3 | New tools, edge case fixes, data moved from hardcode to Excel | ✅ Done |
| Day 4 | Deploy to Hugging Face Spaces | ✅ Done |
| Day 5 | README polish, update resume, LinkedIn post | 🔲 Pending |

---

## Day 1 — Completed ✅

- FastAPI backend with `/chat`, `/reset`, `/health` endpoints
- LangGraph `create_react_agent` with LLaMA 3.3 70B via Groq
- Dark theme HTML/CSS/JS chat UI with suggestion chips and typing indicator
- 6 tools implemented in `tools.py`
- Agent responding correctly to TP lookups and policy queries
- Folder structure and `.gitignore` set up

**Key decisions:**
- Migrated from `AgentExecutor` (removed in LangChain 1.2.x) to LangGraph `create_react_agent`
- Only `llama-3.3-70b-versatile` reliably executes tool calls — 8B models print raw JSON
- Port 7860 (Hugging Face Spaces default)

---

## Day 2 — Completed ✅

- Tools rewritten to read from actual docs folder (not hardcoded)
- Fixed Excel column mapping — `TP Name` not `Company Name`
- ChromaDB vector search integrated into `search_knowledge_base`
  - Docs indexed on first startup, cached on subsequent runs
  - ~83% token reduction vs full-doc loading
- In-memory caching for TP master and doc loading
- Removed Ollama and Cerebras — not viable (GPU too small, 8B can't do tool calling)
- Groq with `llama-3.3-70b-versatile` confirmed as only reliable option
- Committed and pushed to GitHub

---

## Day 3 — Completed ✅

- Added 2 new tools: `detect_sla_breaches` and `get_onboarding_status`
- SLA thresholds set per protocol: SFTP=4h, AS2=2h, FTPS=6h
- SLA simulation seeded with `tp_id + hour` — consistent within session, changes naturally over time
- Onboarding tracker moved from hardcoded dict to `onboarding_tracker.xlsx` in docs/
- Fixed Excel date parsing — datetime objects handled correctly, OVERDUE flag working
- Added `Connection Type` and `Password Reset Allowed` fields to `load_tp_master()`
- `get_tp_details` updated to show new fields
- `draft_escalation_email` now includes password reset warning when JO approval required
- Fixed duplicate `get_onboarding_status` function definition
- Added `recursion_limit: 10` to agent invoke to prevent infinite tool loops
- Registered both new tools in `agent.py` TOOLS list and SYSTEM_PROMPT

---

## Day 4 — Completed ✅

- Created Dockerfile with `python:3.11-slim` base
- Fixed ChromaDB cold start failure — pre-download embedding model at Docker build time
- Created `.dockerignore` to exclude `.env`, `chroma_db`, `__pycache__`
- Updated `requirements.txt` with all 13 required packages
- Added HF Spaces frontmatter to README.md
- Created HF Space (Docker SDK, public, port 7860)
- Set `GROQ_API_KEY` as Space secret
- Pushed to Hugging Face Spaces via Git
- App live and running at https://huggingface.co/spaces/aditya1401/mft-operations-agent

---

## Day 5 — Pending 🔲

- [ ] Test all 8 tools on live URL (Groq limit resets midnight UTC)
- [ ] Final README polish with screenshots
- [ ] Update resume with Project 2
- [ ] LinkedIn post
- [ ] Update progress.md — mark Project 2 complete

---

## Architecture

```
HTML Chat UI (static/index.html)
        ↓ POST /chat
FastAPI (app.py)
        ↓
MFTAgent — LangGraph create_react_agent
        ↓
8 Tools (tools.py)
        ↓
docs/ folder + ChromaDB + SQLite
```

## Tech Stack

- LLM: LLaMA 3.3 70B via Groq
- Agent: LangGraph `create_react_agent`
- Vector DB: ChromaDB (sentence-transformers)
- Backend: FastAPI + Uvicorn
- Frontend: HTML/CSS/Vanilla JS
- Parsing: openpyxl, pdfplumber, python-docx

## GitHub
[github.com/adii1401/mft-operations-agent](https://github.com/adii1401/mft-operations-agent)