# Personal Tracker (Discipline & Self‑Improvement)

A streamlined personal discipline and life‑management app built with Streamlit and SQLite. Track daily wellness, education goals, tasks, projects, and finances — and generate weekly AI insights via Groq’s LLMs.

This repository includes:
- Streamlit UI for daily tracking across focus areas
- SQLite schema and robust CRUD layer
- Tests for CRUD operations, timers, streaks, and integration
- Specs, PRD, and wireframes to guide future work

## Quick Start

- Prerequisites
  - Python 3.11+ recommended
  - Virtual environment tool (e.g., `venv`)
  - Groq API key for AI features

- Install
  - `python -m venv .venv && source .venv/bin/activate`
  - `pip install -r requirements.txt`
  - First run initializes the SQLite DB at `src/database/discipline_tracker.db` (tables created on import)

- Run the app
  - `streamlit run src/main.py`

- Configure secrets
  - Create `.streamlit/secrets.toml` with:
    - `GROQ_API_KEY = "<your_api_key>"`

## Features

- Wellness & Development
  - Water intake, gym completion, food & macros logging
  - Timers for cognitive games and French practice
  - Weekly goals and streak surfacing

- Education
  - Add, list, and update education goals with progress

- Tasks
  - Daily tasks with priority and completion toggles

- Projects
  - Lightweight project tracking with progress and status

- Finance
  - Credit/debit transactions with category, amount, and notes; recent table view

- AI Insights (Groq)
  - Weekly summary, Q&A, and simple correlation analysis using Groq models

## Architecture

- UI: Streamlit single‑page app with tabs (`src/main.py`)
- Data: SQLite (`src/database/discipline_tracker.db`)
- Data access: `src/database/crud.py` provides atomic CRUD with retry on locks
- Schema bootstrap: `src/database/database.py` creates all tables if missing
- Tests: `tests/` cover CRUD, streaks, timers, and end‑to‑end flows
- Specs & docs: `specs/` plus PRD and wireframe PDFs at repo root

## Code Map

- App entry: `src/main.py`
- Database
  - Schema bootstrap: `src/database/database.py`
  - CRUD layer: `src/database/crud.py`
  - Local DB file: `src/database/discipline_tracker.db`
- Tests: `tests/` (`pytest` configured via `pytest.ini`)
- Linting: `ruff.toml`
- Requirements: `requirements.txt`

## Configuration

- Environment
  - Streamlit reads secrets from `.streamlit/secrets.toml`
  - SQLite path is hardcoded: `src/database/discipline_tracker.db`

- Model selection
  - `ChatGroq` initialized with `model_name="qwen/qwen3-32b"` and `temperature=0`

## Data Model (tables)

- users: core profile and targets
- daily_logs: day‑level health and activity metrics
- cognitive_games_sessions: typed sessions with optional difficulty/performance
- french_practice_sessions: typed practice with proficiency and self‑assessment
- news_reading_sessions: articles and notes
- education_goals: goals with status and progress
- tasks_daily: dated prioritised tasks
- projects: basic project portfolio
- financial_transactions: income/expense ledger

See `src/database/database.py` for exact schemas.

## Testing

- Run tests
  - `pytest -q`

- Scope
  - CRUD correctness, locked‑DB retries, task flows, timer logic, and integration

## Development Notes

- Style
  - Keep UI logic in `src/main.py`; prefer small helpers for UI sections
  - Keep all DB access in `src/database/crud.py` with parameterized SQL

- DB concurrency
  - `get_db_connection()` includes exponential backoff on “database is locked” errors

- Streak calculation
  - `calculate_streak()` currently returns a placeholder value; future work should compute from `daily_logs`

- Timers
  - Current timers update Streamlit state with blocking `sleep` loops; consider migrating to session‑safe async or callback patterns for scalability

## Security & Secrets

- Do not commit `.streamlit/secrets.toml` or real API keys
- SQLite file contains personal data — treat `src/database/discipline_tracker.db` as sensitive

## Roadmap Ideas

- Replace placeholder streak logic with real daily‑log aggregation
- Persist timers and counters as sessions in DB
- Add filtering/analytics pages for finance and tasks
- Introduce auth/multi‑user with per‑user secrets storage
- Move DB path to environment variable; support Postgres via SQLAlchemy
- Add export/import (CSV/Parquet) and backups
- Add CI for lint/test and pre‑commit hooks

## Troubleshooting

- Streamlit runs but AI calls fail
  - Ensure `.streamlit/secrets.toml` exists and `GROQ_API_KEY` is set

- "database is locked" errors
  - Retries exist, but long‑running concurrent writes can still fail; avoid simultaneous writes or increase `timeout`

- Tests cannot find DB
  - Ensure tests create or reset `src/database/discipline_tracker.db`; run the app once to initialize tables, or call `src/database/database.py`

## License

- This project does not include a license file. If you plan to distribute, add a suitable license (e.g., MIT) at the repository root.

