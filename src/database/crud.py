import sqlite3
import time

DATABASE_FILE = "src/database/discipline_tracker.db"

def get_db_connection():
    """Get a database connection with retry logic for locked database"""
    max_retries = 5
    retry_delay = 0.1  # seconds
    
    for attempt in range(max_retries):
        try:
            conn = sqlite3.connect(DATABASE_FILE, timeout=20.0)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e) and attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                continue
            else:
                raise e

# User CRUD
def create_user(height, weight, cognitive_games_target_minutes, french_practice_target_minutes, news_reading_target_articles):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (height, weight, cognitive_games_target_minutes, french_practice_target_minutes, news_reading_target_articles) VALUES (?, ?, ?, ?, ?)",
                       (height, weight, cognitive_games_target_minutes, french_practice_target_minutes, news_reading_target_articles))
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def get_user(user_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        return user
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

def update_user(user_id, height=None, weight=None, cognitive_games_target_minutes=None, french_practice_target_minutes=None, news_reading_target_articles=None):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build dynamic query based on provided parameters
        updates = []
        params = []
        
        if height is not None:
            updates.append("height = ?")
            params.append(height)
        if weight is not None:
            updates.append("weight = ?")
            params.append(weight)
        if cognitive_games_target_minutes is not None:
            updates.append("cognitive_games_target_minutes = ?")
            params.append(cognitive_games_target_minutes)
        if french_practice_target_minutes is not None:
            updates.append("french_practice_target_minutes = ?")
            params.append(french_practice_target_minutes)
        if news_reading_target_articles is not None:
            updates.append("news_reading_target_articles = ?")
            params.append(news_reading_target_articles)
            
        updates.append("updated_at = CURRENT_TIMESTAMP")
        
        params.append(user_id)
        
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

# Daily Log CRUD
def create_daily_log(user_id, date, gym_completed, water_ml, calories, protein, carbs, fats, cognitive_games_minutes, cognitive_games_completed, french_practice_minutes, french_practice_completed, news_reading_completed, news_articles_read, goals_completed, streak_eligible):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO daily_logs (user_id, date, gym_completed, water_ml, calories, protein, carbs, fats, cognitive_games_minutes, cognitive_games_completed, french_practice_minutes, french_practice_completed, news_reading_completed, news_articles_read, goals_completed, streak_eligible) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (user_id, date, gym_completed, water_ml, calories, protein, carbs, fats, cognitive_games_minutes, cognitive_games_completed, french_practice_minutes, french_practice_completed, news_reading_completed, news_articles_read, goals_completed, streak_eligible))
        conn.commit()
        log_id = cursor.lastrowid
        return log_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def get_daily_log(log_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM daily_logs WHERE id = ?", (log_id,))
        log = cursor.fetchone()
        return log
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

def get_daily_log_by_date(user_id, date):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM daily_logs WHERE user_id = ? AND date = ?", (user_id, date))
        log = cursor.fetchone()
        return log
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

def update_daily_log(log_id, **kwargs):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build dynamic query based on provided parameters
        updates = []
        params = []
        
        for key, value in kwargs.items():
            updates.append(f"{key} = ?")
            params.append(value)
            
        params.append(log_id)
        
        query = f"UPDATE daily_logs SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def get_weekly_logs(user_id, start_date, end_date):
    """Get daily logs for a specific week"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM daily_logs WHERE user_id = ? AND date BETWEEN ? AND ?", (user_id, start_date, end_date))
        logs = cursor.fetchall()
        return logs
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

# Cognitive Games Session CRUD
def create_cognitive_games_session(user_id, session_date, start_time, end_time, duration_minutes, game_type, difficulty_level, performance_score, performance_notes, session_completed):
    # Validate game_type according to database constraint
    valid_game_types = ['memory', 'logic', 'attention', 'processing_speed', 'Mixed Cognitive Training']
    if game_type not in valid_game_types:
        raise ValueError(f"Invalid game_type. Must be one of: {valid_game_types}")
    
    # Validate difficulty_level according to database constraint
    if difficulty_level is not None and (difficulty_level < 1 or difficulty_level > 10):
        raise ValueError("difficulty_level must be between 1 and 10")
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cognitive_games_sessions (user_id, session_date, start_time, end_time, duration_minutes, game_type, difficulty_level, performance_score, performance_notes, session_completed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (user_id, session_date, start_time, end_time, duration_minutes, game_type, difficulty_level, performance_score, performance_notes, session_completed))
        conn.commit()
        session_id = cursor.lastrowid
        return session_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

# French Practice Session CRUD
def create_french_practice_session(user_id, session_date, start_time, end_time, duration_minutes, practice_type, proficiency_level, practice_notes, self_assessment_score, session_completed):
    # Validate practice_type according to database constraint
    valid_practice_types = ['vocabulary', 'grammar', 'reading', 'listening', 'speaking', 'writing']
    if practice_type not in valid_practice_types:
        raise ValueError(f"Invalid practice_type. Must be one of: {valid_practice_types}")
    
    # Validate proficiency_level according to database constraint
    valid_proficiency_levels = ['beginner', 'intermediate', 'advanced']
    if proficiency_level is not None and proficiency_level not in valid_proficiency_levels:
        raise ValueError(f"Invalid proficiency_level. Must be one of: {valid_proficiency_levels}")
    
    # Validate self_assessment_score according to database constraint
    if self_assessment_score is not None and (self_assessment_score < 1 or self_assessment_score > 10):
        raise ValueError("self_assessment_score must be between 1 and 10")
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO french_practice_sessions (user_id, session_date, start_time, end_time, duration_minutes, practice_type, proficiency_level, practice_notes, self_assessment_score, session_completed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (user_id, session_date, start_time, end_time, duration_minutes, practice_type, proficiency_level, practice_notes, self_assessment_score, session_completed))
        conn.commit()
        session_id = cursor.lastrowid
        return session_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

# News Reading Session CRUD
def create_news_reading_session(user_id, session_date, articles_read, reading_time_minutes, news_categories, key_insights, session_notes):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO news_reading_sessions (user_id, session_date, articles_read, reading_time_minutes, news_categories, key_insights, session_notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (user_id, session_date, articles_read, reading_time_minutes, news_categories, key_insights, session_notes))
        conn.commit()
        session_id = cursor.lastrowid
        return session_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

# Education Goal CRUD
def create_education_goal(user_id, goal_title, goal_description, goal_category, status, progress_percentage):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO education_goals (user_id, goal_title, goal_description, goal_category, status, progress_percentage) VALUES (?, ?, ?, ?, ?, ?)",
                       (user_id, goal_title, goal_description, goal_category, status, progress_percentage))
        conn.commit()
        goal_id = cursor.lastrowid
        return goal_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def get_education_goals(user_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM education_goals WHERE user_id = ?", (user_id,))
        goals = cursor.fetchall()
        return goals
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

def get_education_goal(goal_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM education_goals WHERE id = ?", (goal_id,))
        goal = cursor.fetchone()
        return goal
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

def update_education_goal(goal_id, **kwargs):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build dynamic query based on provided parameters
        updates = []
        params = []
        
        for key, value in kwargs.items():
            updates.append(f"{key} = ?")
            params.append(value)
            
        params.append(goal_id)
        
        query = f"UPDATE education_goals SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def delete_education_goal(goal_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM education_goals WHERE id = ?", (goal_id,))
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

# Daily Task CRUD
def create_daily_task(user_id, date, task_title, task_description, completed, priority):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks_daily (user_id, date, task_title, task_description, completed, priority) VALUES (?, ?, ?, ?, ?, ?)",
                       (user_id, date, task_title, task_description, completed, priority))
        conn.commit()
        task_id = cursor.lastrowid
        return task_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def get_daily_tasks(user_id, date=None):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if date:
            cursor.execute("SELECT * FROM tasks_daily WHERE user_id = ? AND date = ?", (user_id, date))
        else:
            cursor.execute("SELECT * FROM tasks_daily WHERE user_id = ?", (user_id,))
            
        tasks = cursor.fetchall()
        return tasks
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

def get_daily_task(task_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks_daily WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        return task
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

def update_daily_task(task_id, **kwargs):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build dynamic query based on provided parameters
        updates = []
        params = []
        
        for key, value in kwargs.items():
            updates.append(f"{key} = ?")
            params.append(value)
            
        params.append(task_id)
        
        query = f"UPDATE tasks_daily SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def delete_daily_task(task_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks_daily WHERE id = ?", (task_id,))
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def get_weekly_tasks(user_id, start_date, end_date):
    """Get daily tasks for a specific week"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks_daily WHERE user_id = ? AND date BETWEEN ? AND ?", (user_id, start_date, end_date))
        tasks = cursor.fetchall()
        return tasks
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

# Project CRUD
def create_project(user_id, project_name, project_description, progress_percentage, status):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO projects (user_id, project_name, project_description, progress_percentage, status) VALUES (?, ?, ?, ?, ?)",
                       (user_id, project_name, project_description, progress_percentage, status))
        conn.commit()
        project_id = cursor.lastrowid
        return project_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def get_projects(user_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE user_id = ?", (user_id,))
        projects = cursor.fetchall()
        return projects
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

def get_project(project_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        project = cursor.fetchone()
        return project
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

def update_project(project_id, **kwargs):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build dynamic query based on provided parameters
        updates = []
        params = []
        
        for key, value in kwargs.items():
            updates.append(f"{key} = ?")
            params.append(value)
            
        params.append(project_id)
        
        query = f"UPDATE projects SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def delete_project(project_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

# Financial Transaction CRUD
def create_financial_transaction(user_id, transaction_date, transaction_type, category, amount, notes):
    # Validate transaction_type according to database constraint
    valid_transaction_types = ['credit', 'debit']
    if transaction_type not in valid_transaction_types:
        raise ValueError(f"Invalid transaction_type. Must be one of: {valid_transaction_types}")
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO financial_transactions (user_id, transaction_date, transaction_type, category, amount, notes) VALUES (?, ?, ?, ?, ?, ?)",
                       (user_id, transaction_date, transaction_type, category, amount, notes))
        conn.commit()
        transaction_id = cursor.lastrowid
        return transaction_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def get_financial_transactions(user_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM financial_transactions WHERE user_id = ?", (user_id,))
        transactions = cursor.fetchall()
        return transactions
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

def get_financial_transaction(transaction_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM financial_transactions WHERE id = ?", (transaction_id,))
        transaction = cursor.fetchone()
        return transaction
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()

def update_financial_transaction(transaction_id, **kwargs):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build dynamic query based on provided parameters
        updates = []
        params = []
        
        for key, value in kwargs.items():
            updates.append(f"{key} = ?")
            params.append(value)
            
        params.append(transaction_id)
        
        query = f"UPDATE financial_transactions SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def delete_financial_transaction(transaction_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM financial_transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()