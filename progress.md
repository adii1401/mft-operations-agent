# Project 2 — MFT Operations Agent: Progress Tracker

## Goal
Build an AI-powered chat agent for MFT operations support engineers.
Deploy on Hugging Face Spaces by end of Day 5.

---

## Status: Day 2 Complete ✅

---

## Day Plan

| Day | Goal | Status |
|-----|------|--------|
| Day 1 | FastAPI + LangGraph agent + chat UI working locally | ✅ Done |
| Day 2 | Tools reading from docs, ChromaDB vector search, tools stabilized | ✅ Done |
| Day 3 | Fix remaining tool bugs, conversation memory polish, edge cases | 🔲 Pending |
| Day 4 | Deploy to Hugging Face Spaces | 🔲 Pending |
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

**Known issues for Day 3:**
- `get_pending_followups` called wrong tool for "Show overdue follow-ups" query
- `generate_onboarding_checklist` not tested (hit token limit)
- Agent initializes twice on startup (uvicorn behavior — cosmetic, not a bug)

---

## Day 3 — Pending 🔲

- [ ] Fix system prompt for `get_pending_followups` tool description
- [ ] Test all 5 suggestion chips end-to-end
- [ ] Test multi-turn conversation memory
- [ ] Handle edge cases: unknown TP ID, empty follow-ups, unsupported protocol
- [ ] Add requirements.txt with pinned versions

---

## Day 4 — Pending 🔲

- [ ] Create Hugging Face Space
- [ ] Set GROQ_API_KEY as Space secret
- [ ] Push code, verify deployment
- [ ] Test live URL

---

## Day 5 — Pending 🔲

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
6 Tools (tools.py)
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