import pytest
from unittest.mock import patch, MagicMock
from src.database import crud

@pytest.fixture
def mock_db():
    with patch('src.database.crud.get_db_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        yield mock_cursor

def test_create_user(mock_db):
    crud.create_user(180, 80, 30, 20, 3)
    mock_db.execute.assert_called_once()

def test_get_user(mock_db):
    crud.get_user(1)
    mock_db.execute.assert_called_once_with("SELECT * FROM users WHERE id = ?", (1,))

def test_update_user(mock_db):
    crud.update_user(1, height=185, weight=85)
    mock_db.execute.assert_called_once()

def test_create_daily_log(mock_db):
    crud.create_daily_log(1, "2023-06-15", True, 2500, 2000, 150, 200, 80, 30, True, 20, True, True, 3, True, True)
    mock_db.execute.assert_called_once()

def test_get_daily_log(mock_db):
    crud.get_daily_log(1)
    mock_db.execute.assert_called_once_with("SELECT * FROM daily_logs WHERE id = ?", (1,))

def test_get_daily_log_by_date(mock_db):
    crud.get_daily_log_by_date(1, "2023-06-15")
    mock_db.execute.assert_called_once_with("SELECT * FROM daily_logs WHERE user_id = ? AND date = ?", (1, "2023-06-15"))

def test_update_daily_log(mock_db):
    crud.update_daily_log(1, gym_completed=True, water_ml=3000)
    mock_db.execute.assert_called_once()

def test_create_education_goal(mock_db):
    crud.create_education_goal(1, "Learn Python", "Complete Python course", "education", "in_progress", 50)
    mock_db.execute.assert_called_once()

def test_get_education_goals(mock_db):
    crud.get_education_goals(1)
    mock_db.execute.assert_called_once_with("SELECT * FROM education_goals WHERE user_id = ?", (1,))

def test_get_education_goal(mock_db):
    crud.get_education_goal(1)
    mock_db.execute.assert_called_once_with("SELECT * FROM education_goals WHERE id = ?", (1,))

def test_update_education_goal(mock_db):
    crud.update_education_goal(1, status="completed", progress_percentage=100)
    mock_db.execute.assert_called_once()

def test_delete_education_goal(mock_db):
    crud.delete_education_goal(1)
    mock_db.execute.assert_called_once_with("DELETE FROM education_goals WHERE id = ?", (1,))

def test_create_daily_task(mock_db):
    crud.create_daily_task(1, "2023-06-15", "Task 1", "Description", False, 2)
    mock_db.execute.assert_called_once()

def test_get_daily_tasks(mock_db):
    crud.get_daily_tasks(1)
    mock_db.execute.assert_called_once_with("SELECT * FROM tasks_daily WHERE user_id = ?", (1,))

def test_get_daily_task(mock_db):
    crud.get_daily_task(1)
    mock_db.execute.assert_called_once_with("SELECT * FROM tasks_daily WHERE id = ?", (1,))

def test_update_daily_task(mock_db):
    crud.update_daily_task(1, completed=True)
    mock_db.execute.assert_called_once()

def test_delete_daily_task(mock_db):
    crud.delete_daily_task(1)
    mock_db.execute.assert_called_once_with("DELETE FROM tasks_daily WHERE id = ?", (1,))

def test_create_project(mock_db):
    crud.create_project(1, "Project 1", "Description", 50, "in_progress")
    mock_db.execute.assert_called_once()

def test_get_projects(mock_db):
    crud.get_projects(1)
    mock_db.execute.assert_called_once_with("SELECT * FROM projects WHERE user_id = ?", (1,))

def test_get_project(mock_db):
    crud.get_project(1)
    mock_db.execute.assert_called_once_with("SELECT * FROM projects WHERE id = ?", (1,))

def test_update_project(mock_db):
    crud.update_project(1, status="completed", progress_percentage=100)
    mock_db.execute.assert_called_once()

def test_delete_project(mock_db):
    crud.delete_project(1)
    mock_db.execute.assert_called_once_with("DELETE FROM projects WHERE id = ?", (1,))

def test_create_financial_transaction_invalid_type(mock_db):
    # Test that invalid transaction types raise an error
    with pytest.raises(ValueError):
        crud.create_financial_transaction(1, "2023-06-15", "Income", "Food", 25.50, "Lunch")

def test_create_cognitive_games_session_invalid_type(mock_db):
    # Test that invalid game types raise an error
    with pytest.raises(ValueError):
        crud.create_cognitive_games_session(
            user_id=1,
            session_date="2023-06-15",
            start_time="10:00:00",
            end_time="10:30:00",
            duration_minutes=30,
            game_type="invalid_game",
            difficulty_level=5,
            performance_score=80,
            performance_notes="Good performance",
            session_completed=True
        )

def test_create_cognitive_games_session_invalid_difficulty(mock_db):
    # Test that invalid difficulty levels raise an error
    with pytest.raises(ValueError):
        crud.create_cognitive_games_session(
            user_id=1,
            session_date="2023-06-15",
            start_time="10:00:00",
            end_time="10:30:00",
            duration_minutes=30,
            game_type="memory",
            difficulty_level=15,  # Invalid - should be 1-10
            performance_score=80,
            performance_notes="Good performance",
            session_completed=True
        )

def test_create_french_practice_session_invalid_type(mock_db):
    # Test that invalid practice types raise an error
    with pytest.raises(ValueError):
        crud.create_french_practice_session(
            user_id=1,
            session_date="2023-06-15",
            start_time="10:00:00",
            end_time="10:30:00",
            duration_minutes=30,
            practice_type="invalid_practice",
            proficiency_level="beginner",
            practice_notes="Good practice",
            self_assessment_score=8,
            session_completed=True
        )

def test_create_french_practice_session_invalid_proficiency(mock_db):
    # Test that invalid proficiency levels raise an error
    with pytest.raises(ValueError):
        crud.create_french_practice_session(
            user_id=1,
            session_date="2023-06-15",
            start_time="10:00:00",
            end_time="10:30:00",
            duration_minutes=30,
            practice_type="vocabulary",
            proficiency_level="expert",  # Invalid - should be beginner/intermediate/advanced
            practice_notes="Good practice",
            self_assessment_score=8,
            session_completed=True
        )

def test_create_french_practice_session_invalid_score(mock_db):
    # Test that invalid self assessment scores raise an error
    with pytest.raises(ValueError):
        crud.create_french_practice_session(
            user_id=1,
            session_date="2023-06-15",
            start_time="10:00:00",
            end_time="10:30:00",
            duration_minutes=30,
            practice_type="vocabulary",
            proficiency_level="beginner",
            practice_notes="Good practice",
            self_assessment_score=15,  # Invalid - should be 1-10
            session_completed=True
        )

def test_get_financial_transactions(mock_db):
    crud.get_financial_transactions(1)
    mock_db.execute.assert_called_once_with("SELECT * FROM financial_transactions WHERE user_id = ?", (1,))

def test_get_financial_transaction(mock_db):
    crud.get_financial_transaction(1)
    mock_db.execute.assert_called_once_with("SELECT * FROM financial_transactions WHERE id = ?", (1,))

def test_update_financial_transaction(mock_db):
    crud.update_financial_transaction(1, amount=30.00)
    mock_db.execute.assert_called_once()

def test_delete_financial_transaction(mock_db):
    crud.delete_financial_transaction(1)
    mock_db.execute.assert_called_once_with("DELETE FROM financial_transactions WHERE id = ?", (1,))

def test_create_financial_transaction_valid_credit(mock_db):
    crud.create_financial_transaction(1, "2023-06-15", "credit", "Salary", 2500.00, "Monthly salary")
    mock_db.execute.assert_called_once()
