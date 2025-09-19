# Data Model

Based on the feature specification and PRD, the following data model will be used.

## Tables

### users
- id (INTEGER, PRIMARY KEY)
- height (REAL)
- weight (REAL)
- cognitive_games_target_minutes (INTEGER)
- french_practice_target_minutes (INTEGER)
- news_reading_target_articles (INTEGER)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

### daily_logs
- id (INTEGER, PRIMARY KEY)
- user_id (INTEGER, FOREIGN KEY)
- date (DATE)
- gym_completed (BOOLEAN)
- water_ml (INTEGER)
- calories (REAL)
- protein (REAL)
- carbs (REAL)
- fats (REAL)
- cognitive_games_minutes (INTEGER)
- cognitive_games_completed (BOOLEAN)
- french_practice_minutes (INTEGER)
- french_practice_completed (BOOLEAN)
- news_reading_completed (BOOLEAN)
- news_articles_read (INTEGER)
- goals_completed (BOOLEAN)
- streak_eligible (BOOLEAN)

### cognitive_games_sessions
- id (INTEGER, PRIMARY KEY)
- user_id (INTEGER, FOREIGN KEY)
- session_date (DATE)
- start_time (TIMESTAMP)
- end_time (TIMESTAMP)
- duration_minutes (INTEGER)
- game_type (TEXT)
- difficulty_level (INTEGER)
- performance_score (INTEGER)
- performance_notes (TEXT)
- session_completed (BOOLEAN)
- created_at (TIMESTAMP)

### french_practice_sessions
- id (INTEGER, PRIMARY KEY)
- user_id (INTEGER, FOREIGN KEY)
- session_date (DATE)
- start_time (TIMESTAMP)
- end_time (TIMESTAMP)
- duration_minutes (INTEGER)
- practice_type (TEXT)
- proficiency_level (TEXT)
- practice_notes (TEXT)
- self_assessment_score (INTEGER)
- session_completed (BOOLEAN)
- created_at (TIMESTAMP)

### news_reading_sessions
- id (INTEGER, PRIMARY KEY)
- user_id (INTEGER, FOREIGN KEY)
- session_date (DATE)
- articles_read (INTEGER)
- reading_time_minutes (INTEGER)
- news_categories (TEXT)
- key_insights (TEXT)
- session_notes (TEXT)
- created_at (TIMESTAMP)

### education_goals
- id (INTEGER, PRIMARY KEY)
- user_id (INTEGER, FOREIGN KEY)
- goal_title (TEXT)
- goal_description (TEXT)
- goal_category (TEXT)
- status (TEXT)
- progress_percentage (INTEGER)
- created_at (TIMESTAMP)

### tasks_daily
- id (INTEGER, PRIMARY KEY)
- user_id (INTEGER, FOREIGN KEY)
- date (DATE)
- task_title (TEXT)
- task_description (TEXT)
- completed (BOOLEAN)
- priority (INTEGER)

### projects
- id (INTEGER, PRIMARY KEY)
- user_id (INTEGER, FOREIGN KEY)
- project_name (TEXT)
- project_description (TEXT)
- progress_percentage (INTEGER)
- status (TEXT)
- created_at (TIMESTAMP)

### financial_transactions
- id (INTEGER, PRIMARY KEY)
- user_id (INTEGER, FOREIGN KEY)
- transaction_date (DATE)
- transaction_type (TEXT)
- category (TEXT)
- amount (REAL)
- notes (TEXT)
