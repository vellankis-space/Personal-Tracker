# Tasks: Comprehensive Discipline & Self-Improvement Tracker

**Input**: Design documents from `/specs/001-i-am-in/`
**Prerequisites**: plan.md, data-model.md, quickstart.md

## Phase 3.1: Setup
- [x] T001: Set up the project structure with `src` and `tests` directories.
- [x] T002: Create a virtual environment and install dependencies: `streamlit`, `langchain`, `groq`, `pytest`.
- [x] T003: [P] Configure `ruff` for linting and formatting.

## Phase 3.2: Database
- [x] T004: Create the SQLite database file `discipline_tracker.db` in `src/database/`.
- [x] T005: [P] Implement the database creation script in `src/database/database.py` to create all tables as defined in `data-model.md`.
- [x] T006: [P] Implement CRUD functions for the `users` table in `src/database/crud.py`.
- [x] T007: [P] Implement CRUD functions for the `daily_logs` table in `src/database/crud.py`.
- [x] T008: [P] Implement CRUD functions for the `cognitive_games_sessions` table in `src/database/crud.py`.
- [x] T009: [P] Implement CRUD functions for the `french_practice_sessions` table in `src/database/crud.py`.
- [x] T010: [P] Implement CRUD functions for the `news_reading_sessions` table in `src/database/crud.py`.
- [x] T011: [P] Implement CRUD functions for the `education_goals` table in `src/database/crud.py`.
- [x] T012: [P] Implement CRUD functions for the `tasks_daily` table in `src/database/crud.py`.
- [x] T013: [P] Implement CRUD functions for the `projects` table in `src/database/crud.py`.
- [x] T014: [P] Implement CRUD functions for the `financial_transactions` table in `src/database/crud.py`.

## Phase 3.3: Backend (Streamlit) Implementation
- [x] T015: Create the main application file `src/main.py`.
- [x] T016: Implement the main navigation tabs using `st.tabs` in `src/main.py`.
- [x] T017: [P] Implement the top navigation bar with metrics and progress bars in `src/main.py`.
- [x] T018: [P] Implement the 'Wellness & Development' tab UI in `src/main.py`.
- [x] T019: Implement the logic for the water intake tracker in `src/main.py`.
- [x] T020: Implement the logic for the gym attendance tracker in `src/main.py`.
- [x] T021: Implement the logic for the food and macros tracker in `src/main.py`.
- [x] T022: Implement the cognitive games timer with start/pause/resume functionality in `src/main.py`.
- [x] T023: Implement the French practice timer with start/pause/resume functionality in `src/main.py`.
- [x] T024: Implement the news reading tracker in `src/main.py`.
- [x] T025: Implement the weekly goals and streak system in `src/main.py`.
- [x] T026: [P] Implement the 'Education' tab UI and logic in `src/main.py`.
- [x] T027: [P] Implement the 'Tasks' tab UI and logic in `src/main.py`.
- [x] T028: [P] Implement the 'Projects' tab UI and logic in `src/main.py`.
- [x] T029: [P] Implement the 'Finance' tab UI and logic in `src/main.py`.

## Phase 3.4: AI Integration
- [x] T030: Configure LangChain with the Groq API in `src/main.py`.
- [x] T031: Implement the weekly AI summary generation in the 'AI Insights' tab.
- [x] T032: Implement the natural language query interface in the 'AI Insights' tab.
- [x] T033: Implement the cross-activity correlation analysis and display AI-powered advice.

## Phase 3.5: Testing
- [x] T034: [P] Write unit tests for all CRUD functions in `tests/test_crud.py`.
- [x] T035: [P] Write unit tests for the timer logic in `tests/test_timers.py`.
- [x] T036: [P] Write unit tests for the streak logic in `tests/test_streaks.py`.
- [x] T037: Write integration tests for the main application flow in `tests/test_integration.py`.

## Dependencies
- T001, T002, T003 must be completed before all other tasks.
- T004, T005 must be completed before T006-T014.
- T006-T014 can be run in parallel.
- Database tasks (T004-T014) must be completed before backend implementation (T015-T029).
- Backend implementation tasks can be parallelized where they don't conflict.
- AI integration (T030-T033) depends on the backend implementation.
- Testing tasks (T034-T037) should be written alongside the implementation (TDD).

## Parallel Example
```
# Launch T006-T014 together:
Task: "Implement CRUD functions for the users table in src/database/crud.py"
Task: "Implement CRUD functions for the daily_logs table in src/database/crud.py"
...
```