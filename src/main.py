import streamlit as st
from langchain_groq import ChatGroq
import os
import sys
import pandas as pd
sys.path.append('src/database')
from crud import (
    create_user, get_user, update_user,
    create_daily_log, get_daily_log, get_daily_log_by_date, update_daily_log, get_weekly_logs,
    create_education_goal, get_education_goals, get_education_goal, update_education_goal, delete_education_goal,
    create_daily_task, get_daily_tasks, get_daily_task, update_daily_task, delete_daily_task, get_weekly_tasks,
    create_project, get_projects, get_project, update_project, delete_project,
    create_financial_transaction, get_financial_transactions, get_financial_transaction, update_financial_transaction, delete_financial_transaction
)
import datetime

def section_header(text: str, center: bool = False):
    align = "text-align:center;" if center else ""
    st.markdown("<div class='container section-tight'>", unsafe_allow_html=True)
    st.markdown(
        f"<h3 style='margin-top:8px; margin-bottom:4px; {align} background: linear-gradient(90deg, var(--brand), var(--brand-2)); -webkit-background-clip:text; background-clip:text; color: transparent;'>"+text+"</h3>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Configure Groq API
api_key = st.secrets["GROQ_API_KEY"]
chat = ChatGroq(temperature=0, groq_api_key=api_key, model_name="qwen/qwen3-32b")

def calculate_streak(user_id):
    """
    Calculate the current streak based on daily logs.
    A streak is maintained if goals are completed each day.
    """
    # For now, return a default streak value
    # In a real implementation, this would calculate based on daily logs
    try:
        # Get recent daily logs to calculate streak
        today = datetime.date.today()
        # In a real implementation, we would query the database for recent logs
        # and calculate the streak based on consecutive days with goals completed
        return 3  # Default value for now
    except Exception as e:
        # Return default streak if there's an error
        return 3

def _inject_global_styles():
    st.markdown(
        """
        <style>
        :root, .theme-dark {
          --bg: #0b1020;
          --card: #111834;
          --ink: #E6E9F5;
          --muted: #9AA3B2;
          --brand: #7C5CFF;
          --brand-2: #24D3EE;
          --good: #22c55e;
          --warn: #f59e0b;
          --bad: #ef4444;
          --radius: 16px;
        }
        .stApp { background: radial-gradient(1200px 800px at 10% -10%, rgba(26,34,71,.9) 0%, var(--bg) 35%) fixed; transition: background-color .35s ease; }
        /* Minimal layout adjustments */
        section.main > div { padding-top: 1rem; }
        .glass {
          background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: var(--radius);
          box-shadow: 0 10px 30px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.04);
          padding: 1rem 1.25rem;
          transition: transform .12s ease, box-shadow .25s ease, background .35s ease, border-color .35s ease;
        }
        .glass:focus-within, .glass:hover { transform: translateY(-1px); box-shadow: 0 12px 38px rgba(0,0,0,0.4); outline: none; }
        .card-row { display:flex; gap:12px; align-items:flex-start; }
        .card-title { font-weight:700; color:var(--ink); }
        .pill { padding:.25rem .6rem; border-radius:999px; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.08); font-size:.75rem; color:var(--muted); }
        .pill.success { color: var(--good); border-color: rgba(34,197,94,.35); }
        .pill.warn { color: var(--warn); border-color: rgba(245,158,11,.35); }
        .pill.info { color: var(--brand-2); border-color: rgba(36,211,238,.35); }
        .act { display:inline-flex; align-items:center; gap:.35rem; padding:.35rem .6rem; border-radius:10px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); color:var(--ink); font-size:.8rem; cursor:pointer; }
        .act:hover { background: rgba(255,255,255,0.07); }
        .act[aria-pressed="true"] { outline: 2px solid var(--brand-2); }
        .sr-only { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); border:0; }
        }
        .metric-card {
          display: flex; align-items: center; gap: .75rem;
          color: var(--ink);
        }
        .metric-icon { font-size: 1.2rem; }
        .metric-label { font-size: .8rem; color: var(--muted); }
        .metric-value { font-size: 1.15rem; font-weight: 700; }
        .ring {
          --size: 64px; --bar: 8px; --val: 0.0; --grad: linear-gradient(90deg,var(--brand),var(--brand-2));
          width: var(--size); height: var(--size); border-radius: 50%; position: relative;
          background:
            radial-gradient(farthest-side, var(--card) calc(50% - var(--bar)), transparent 0 99.9%, var(--card) 0),
            conic-gradient(from -90deg, var(--grad) calc(var(--val)*1%), rgba(255,255,255,0.08) 0);
          transition: background .6s ease;
        }
        .ring::after{ content:""; position:absolute; inset: calc(var(--bar) + 6px); background: var(--card); border-radius:50%; }
        .ring-label{ position:absolute; inset:0; display:grid; place-items:center; color:var(--ink); font-size:.85rem; font-weight:700; }
        .streak {
          display:flex; align-items:center; gap:.6rem; color:var(--ink);
        }
        .streak .flame { filter: drop-shadow(0 0 12px rgba(255,161,22,.45)); font-size: 1.4rem; }
        .pill { padding:.25rem .6rem; border-radius:999px; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.08); font-size:.75rem; color:var(--muted); }
        h1.app-title { font-weight:800; letter-spacing:.3px; font-size:1.8rem; margin: .25rem 0 .5rem; background: linear-gradient(90deg, var(--brand), var(--brand-2)); -webkit-background-clip:text; background-clip:text; color:transparent; }
        .sub { color: var(--muted); margin-bottom: .75rem; }
        .hr { height:1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent); margin:.5rem 0 1rem; }
        .btn-row button[kind="secondary"] { border-radius:10px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _header(title: str, subtitle: str | None = None):
    st.markdown(f"<h1 class='app-title'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='sub'>{subtitle}</div>", unsafe_allow_html=True)
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)


def _ring_progress(label: str, value: float, caption: str = ""):
    # Define icons for each label
    icons = {
        "Water": "💧",
        "Cognitive": "🧠",
        "French": "🇫🇷",
        "Progress": "📊"
    }
    icon = icons.get(label, "📊")  # Default icon if not found
    
    pct = max(0.0, min(1.0, value))
    html = f"""
    <div class="glass" style="display:flex; align-items:center; gap:12px;">
      <div style="font-size: 1.5rem;">{icon}</div>
      <div class="ring" role="img" aria-label="{label} {int(pct*100)} percent" title="{label}: {int(pct*100)}%" style="--val:{pct*100:.2f}">
        <div class="ring-label">{int(pct*100)}%</div>
      </div>
      <div>
        <div class="metric-label" aria-hidden="true">{label}</div>
        <div class="metric-value">{caption}</div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def _streak_count(days: int):
    html = f"""
    <div class="glass streak" role="group" aria-label="User streak">
      <span class="flame" role="img" aria-label="fire" style="font-size: 1.5rem; filter: drop-shadow(0 0 8px rgba(255,161,22,.6));">🔥</span>
      <span class="metric-value">{days} day streak</span>
      <span class="pill info" title="Tip: complete all daily goals to extend streak">Keep it going</span>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def main():
    _inject_global_styles()
    _header("Discipline & Self-Improvement", "Track, reflect, and level up daily")
    
    # Initialize user
    if 'user_id' not in st.session_state:
        # Check if user exists, if not create one
        user = get_user(1)  # Try to get the first user
        if user is None:
            # Create a default user
            user_id = create_user(
                height=175.0,
                weight=72.0,
                cognitive_games_target_minutes=30,
                french_practice_target_minutes=20,
                news_reading_target_articles=3
            )
            st.session_state.user_id = user_id
        else:
            st.session_state.user_id = user['id']
    
    # Get current user
    user = get_user(st.session_state.user_id)

    # Remove theme toggle per request

    # Keep summary row compact without extra containers
    top1, top2, top3, top4 = st.columns([1.2, 1, 1, 1])
    with top1:
        st.markdown(
            f"""
            <div class="glass metric-card">
              <div class="metric-icon" style="font-size: 1.5rem;">📏</div>
              <div>
                <div class="metric-label">Height</div>
                <div class="metric-value">{user['height'] if user else 175} cm</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top2:
        st.markdown(
            f"""
            <div class="glass metric-card">
              <div class="metric-icon" style="font-size: 1.5rem;">⚖️</div>
              <div>
                <div class="metric-label">Weight</div>
                <div class="metric-value">{user['weight'] if user else 72} kg</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top3:
        streak = calculate_streak(st.session_state.user_id)
        _streak_count(streak)
    with top4:
        st.markdown("<div class='pill' title='At-a-glance status for today'>Today’s snapshot</div>", unsafe_allow_html=True)

    # Snapshot rings driven by session values (fallbacks preserved)
    water_target_l = 3.0
    water_l = (st.session_state.get('water_intake', 0) or 0) / 1000.0
    # sqlite3.Row supports dict-style indexing but not .get
    cog_target = (user['cognitive_games_target_minutes'] if user and 'cognitive_games_target_minutes' in user.keys() else 30)
    fr_target = (user['french_practice_target_minutes'] if user and 'french_practice_target_minutes' in user.keys() else 20)
    cog_done = st.session_state.get('cognitive_timer', 0) // 60
    fr_done = st.session_state.get('french_timer', 0) // 60

    # Snapshot rings row directly
    ring1, ring2, ring3 = st.columns(3)
    with ring1:
        _ring_progress("Water", min(water_l / water_target_l, 1.0), f"{water_l:.1f} / {water_target_l:.1f} L")
    with ring2:
        _ring_progress("Cognitive", min(cog_done / float(cog_target or 1), 1.0), f"{int(cog_done)} / {int(cog_target)} min")
    with ring3:
        _ring_progress("French", min(fr_done / float(fr_target or 1), 1.0), f"{int(fr_done)} / {int(fr_target)} min")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Wellness & Development", "Education", "Tasks", "Projects", "Finance", "AI Insights"])

    with tab1:
        section_header("Wellness & Development", center=True)

        # Today's Progress
        section_header("Today's Progress")
        if 'water_intake' not in st.session_state:
            st.session_state.water_intake = 0

        if st.button("Add 250ml Water"):
            st.session_state.water_intake += 250
        
        st.info(f"Water Intake: {st.session_state.water_intake} ml")

        if 'gym_completed' not in st.session_state:
            st.session_state.gym_completed = False

        st.session_state.gym_completed = st.checkbox("Gym Completed", value=st.session_state.gym_completed)

        section_header("Food & Macros")
        calories = st.number_input("Calories", value=0)
        protein = st.number_input("Protein (g)", value=0)
        carbs = st.number_input("Carbs (g)", value=0)
        fats = st.number_input("Fats (g)", value=0)

        # Intellectual Development Center
        section_header("Intellectual Development Center")
        
        # Cognitive Games Timer
        section_header("Cognitive Games Timer")
        if 'cognitive_timer_active' not in st.session_state:
            st.session_state.cognitive_timer_active = False
        if 'cognitive_timer' not in st.session_state:
            st.session_state.cognitive_timer = 0

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Start Cognitive Timer"):
                st.session_state.cognitive_timer_active = True
        with col2:
            if st.button("Pause Cognitive Timer"):
                st.session_state.cognitive_timer_active = False
        with col3:
            if st.button("Reset Cognitive Timer"):
                st.session_state.cognitive_timer = 0

        timer_placeholder = st.empty()

        import time
        while st.session_state.cognitive_timer_active:
            mins, secs = divmod(st.session_state.cognitive_timer, 60)
            timer_placeholder.metric("Cognitive Timer", f"{mins:02d}:{secs:02d}")
            time.sleep(1)
            st.session_state.cognitive_timer += 1

        # French Practice Timer
        section_header("French Practice Timer")
        if 'french_timer_active' not in st.session_state:
            st.session_state.french_timer_active = False
        if 'french_timer' not in st.session_state:
            st.session_state.french_timer = 0

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Start French Timer"):
                st.session_state.french_timer_active = True
        with col2:
            if st.button("Pause French Timer"):
                st.session_state.french_timer_active = False
        with col3:
            if st.button("Reset French Timer"):
                st.session_state.french_timer = 0

        french_timer_placeholder = st.empty()

        while st.session_state.french_timer_active:
            mins, secs = divmod(st.session_state.french_timer, 60)
            french_timer_placeholder.metric("French Timer", f"{mins:02d}:{secs:02d}")
            time.sleep(1)
            st.session_state.french_timer += 1

        # News Reading Tracker
        section_header("News Reading Tracker")
        articles_read = st.number_input("Articles Read", value=0, step=1)

        # Weekly Goals
        section_header("Weekly Goals")
        
        # Initialize session state for weekly goals
        if 'weekly_goals' not in st.session_state:
            st.session_state.weekly_goals = []
        
        # Get current education goals for the user (which can serve as weekly goals)
        education_goals = get_education_goals(st.session_state.user_id)
        
        # UI for setting weekly goals
        st.write("Set your weekly goals:")
        new_goal = st.text_input("New weekly goal")
        if st.button("Add Weekly Goal"):
            if new_goal:
                # Save to database as an education goal
                create_education_goal(
                    user_id=st.session_state.user_id,
                    goal_title=new_goal,
                    goal_description="Weekly goal",
                    goal_category="weekly",
                    status="in_progress",
                    progress_percentage=0
                )
                st.success(f"Added goal: {new_goal}")
                st.rerun()  # Refresh to show updated goals
        
        # Display current weekly goals
        if education_goals:
            st.write("Your weekly goals:")
            for i, goal in enumerate(education_goals):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"- {goal['goal_title']}")
                with col2:
                    # Show progress if available
                    if goal['progress_percentage']:
                        st.write(f"{goal['progress_percentage']}%")
                with col3:
                    # Add checkbox for completion
                    completed = st.checkbox("Completed", key=f"goal_{goal['id']}")
                    if completed and goal['status'] != 'completed':
                        # Update goal status in database
                        update_education_goal(goal['id'], status='completed', progress_percentage=100)
                    elif not completed and goal['status'] == 'completed':
                        # Reset goal status if unchecked
                        update_education_goal(goal['id'], status='in_progress', progress_percentage=50)
        else:
            st.write("No weekly goals set yet.")

    with tab2:
        section_header("Education", center=True)
        section_header("Manage Education Goals")
        goal_title = st.text_input("Goal Title")
        goal_description = st.text_area("Goal Description")
        if st.button("Add Education Goal"):
            if goal_title:
                create_education_goal(
                    user_id=st.session_state.user_id,
                    goal_title=goal_title,
                    goal_description=goal_description,
                    goal_category="education",
                    status="in_progress",
                    progress_percentage=0
                )
                st.success("Education goal added!")
                st.rerun()
        
        # Display existing education goals
        section_header("Your Education Goals")
        education_goals = get_education_goals(st.session_state.user_id)
        if education_goals:
            for goal in education_goals:
                if goal['goal_category'] == 'education':  # Only show education goals, not weekly goals
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{goal['goal_title']}**")
                        st.write(goal['goal_description'])
                    with col2:
                        st.write(f"Status: {goal['status']}")
                    with col3:
                        progress = goal['progress_percentage'] if goal['progress_percentage'] else 0
                        st.progress(progress / 100.0)
        else:
            st.info("No education goals yet. Add one above!")

    with tab3:
        section_header("Tasks", center=True)
        section_header("Manage Daily Tasks")
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Task Description")
        task_date = st.date_input("Task Date", datetime.date.today())
        task_priority = st.selectbox("Priority", [1, 2, 3], format_func=lambda x: ["Low", "Medium", "High"][x-1])
        
        if st.button("Add Task"):
            if task_title:
                create_daily_task(
                    user_id=st.session_state.user_id,
                    date=task_date.isoformat(),
                    task_title=task_title,
                    task_description=task_description,
                    completed=False,
                    priority=task_priority
                )
                st.success("Task added!")
                st.rerun()
        
        # Display existing tasks for today
        section_header("Today's Tasks")
        today = datetime.date.today().isoformat()
        daily_tasks = get_daily_tasks(st.session_state.user_id, today)
        
        if daily_tasks:
            for task in daily_tasks:
                priority_text = ["Low", "Medium", "High"][task['priority']-1]
                aria = f"Task {task['task_title']} priority {priority_text}"
                st.markdown(
                    f"""
                    <div class='glass' role='group' aria-label='{aria}'>
                      <div class='card-row'>
                        <div style='flex:1'>
                          <div class='card-title'>{task['task_title']}</div>
                          <div class='metric-label'>{task['task_description'] or ''}</div>
                        </div>
                        <div class='pill {'success' if task['completed'] else 'warn'}' title='Priority'>Priority: {priority_text}</div>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                # Inline actions: complete toggle
                completed_toggle = st.toggle("Mark complete", value=task['completed'], key=f"toggle_task_{task['id']}", help="Toggle completion status")
                if completed_toggle != task['completed']:
                    update_daily_task(task['id'], completed=completed_toggle)
        else:
            st.info("No tasks for today. Add one above!")

    with tab4:
        section_header("Projects", center=True)
        section_header("Manage Projects")
        project_name = st.text_input("Project Name")
        project_description = st.text_area("Project Description")
        if st.button("Add Project"):
            if project_name:
                create_project(
                    user_id=st.session_state.user_id,
                    project_name=project_name,
                    project_description=project_description,
                    progress_percentage=0,
                    status="planning"
                )
                st.success("Project added!")
                st.rerun()
        
        # Display existing projects
        section_header("Your Projects")
        projects = get_projects(st.session_state.user_id)
        
        if projects:
            for project in projects:
                progress = project['progress_percentage'] if project['progress_percentage'] else 0
                status_pill = 'success' if progress >= 100 else 'info'
                st.markdown(
                    f"""
                    <div class='glass' role='group' aria-label='Project {project['project_name']} status {project['status']}'>
                      <div class='card-row'>
                        <div style='flex:1'>
                          <div class='card-title'>{project['project_name']}</div>
                          <div class='metric-label'>{project['project_description'] or ''}</div>
                        </div>
                        <div class='pill {status_pill}' title='Status'>{project['status'].title()}</div>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                _ring_progress("Progress", (progress or 0)/100.0, f"{progress}%")
        else:
            st.info("No projects yet. Add one above!")

    with tab5:
        section_header("Finance", center=True)
        section_header("Manage Financial Transactions")
        transaction_date = st.date_input("Date", datetime.date.today())
        transaction_type = st.selectbox("Transaction Type", ["credit", "debit"], format_func=lambda x: "Income" if x == "credit" else "Expense")
        category = st.text_input("Category")
        amount = st.number_input("Amount")
        notes = st.text_area("Notes")
        if st.button("Add Transaction"):
            if category and amount > 0:
                create_financial_transaction(
                    user_id=st.session_state.user_id,
                    transaction_date=transaction_date.isoformat(),
                    transaction_type=transaction_type,  # This will be 'credit' or 'debit'
                    category=category,
                    amount=amount,
                    notes=notes
                )
                st.success("Transaction added!")
                st.rerun()
        
        # Display recent transactions
        section_header("Recent Transactions")
        transactions = get_financial_transactions(st.session_state.user_id)
        
        if transactions:
            # Sort by date (newest first)
            sorted_transactions = sorted(transactions, key=lambda x: x['transaction_date'], reverse=True)
            
            # Display as a table using Streamlit's table function
            table_data = []
            for transaction in sorted_transactions[:10]:  # Show last 10 transactions
                # Display user-friendly names
                type_display = "Income" if transaction['transaction_type'] == 'credit' else "Expense"
                amount_display = f"${transaction['amount']:.2f}"
                table_data.append({
                    "Date": transaction['transaction_date'],
                    "Category": transaction['category'],
                    "Type": type_display,
                    "Amount": amount_display,
                    "Notes": transaction['notes'] if transaction['notes'] else ""
                })
            
            # Create a DataFrame and display it
            import pandas as pd
            df = pd.DataFrame(table_data)
            st.dataframe(df)
        else:
            st.info("No transactions yet. Add one above!")

    with tab6:
        section_header("AI Insights", center=True)
        section_header("Weekly AI Summary")
        if st.button("Generate Weekly Summary"):
            # In a real application, you would fetch the user's data from the database
            user_data = "This week, I went to the gym 3 times, drank 2L of water on average, and practiced French for 60 minutes."
            prompt = f"Generate a summary of my week based on the following data:\n{user_data}"
            summary = chat.invoke(prompt).content
            st.write(summary)

        section_header("Ask a question")
        question = st.text_input("Ask a question about your progress")
        if question:
            # In a real application, you would fetch relevant data from the database
            user_data = "This week, I went to the gym 3 times, drank 2L of water on average, and practiced French for 60 minutes."
            prompt = f"Answer the following question based on my progress data:\n{user_data}\n\nQuestion: {question}"
            answer = chat.invoke(prompt).content
            st.write(answer)

        section_header("Cross-Activity Correlation Analysis")
        if st.button("Analyze Correlations"):
            # In a real application, you would fetch and process data from the database
            user_data = "Data: Cognitive game scores improved by 15% on days after French practice."
            prompt = f"Analyze the following correlation and provide advice:\n{user_data}"
            analysis = chat.invoke(prompt).content
            st.write(analysis)

if __name__ == "__main__":
    main()
