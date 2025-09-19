import pytest
from streamlit.testing.v1 import AppTest

def test_app_loads():
    """Test that the app loads without errors."""
    at = AppTest.from_file("src/main.py").run()
    assert not at.exception

def test_streak_logic():
    """Test that the streak calculation function works."""
    # Import and test the streak calculation function directly
    from src.main import calculate_streak
    streak = calculate_streak(1)
    assert isinstance(streak, int)
    assert streak >= 0
