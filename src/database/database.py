import sqlite3


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def main():
    database = r"src/database/discipline_tracker.db"

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        height real,
                                        weight real,
                                        cognitive_games_target_minutes integer,
                                        french_practice_target_minutes integer,
                                        news_reading_target_articles integer,
                                        created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                        updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
                                    ); """

    sql_create_daily_logs_table = """CREATE TABLE IF NOT EXISTS daily_logs (
                                    id integer PRIMARY KEY,
                                    user_id integer NOT NULL,
                                    date text NOT NULL,
                                    gym_completed boolean,
                                    water_ml integer,
                                    calories real,
                                    protein real,
                                    carbs real,
                                    fats real,
                                    cognitive_games_minutes integer,
                                    cognitive_games_completed boolean,
                                    french_practice_minutes integer,
                                    french_practice_completed boolean,
                                    news_reading_completed boolean,
                                    news_articles_read integer,
                                    goals_completed boolean,
                                    streak_eligible boolean,
                                    FOREIGN KEY (user_id) REFERENCES users (id)
                                );"""

    sql_create_cognitive_games_sessions_table = """CREATE TABLE IF NOT EXISTS cognitive_games_sessions (
                                id integer PRIMARY KEY,
                                user_id integer NOT NULL,
                                session_date text NOT NULL,
                                start_time timestamp,
                                end_time timestamp,
                                duration_minutes integer,
                                game_type text,
                                difficulty_level integer,
                                performance_score integer,
                                performance_notes text,
                                session_completed boolean,
                                created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (user_id) REFERENCES users (id)
                            );"""

    sql_create_french_practice_sessions_table = """CREATE TABLE IF NOT EXISTS french_practice_sessions (
                                id integer PRIMARY KEY,
                                user_id integer NOT NULL,
                                session_date text NOT NULL,
                                start_time timestamp,
                                end_time timestamp,
                                duration_minutes integer,
                                practice_type text,
                                proficiency_level text,
                                practice_notes text,
                                self_assessment_score integer,
                                session_completed boolean,
                                created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (user_id) REFERENCES users (id)
                            );"""

    sql_create_news_reading_sessions_table = """CREATE TABLE IF NOT EXISTS news_reading_sessions (
                                id integer PRIMARY KEY,
                                user_id integer NOT NULL,
                                session_date text NOT NULL,
                                articles_read integer,
                                reading_time_minutes integer,
                                news_categories text,
                                key_insights text,
                                session_notes text,
                                created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (user_id) REFERENCES users (id)
                            );"""

    sql_create_education_goals_table = """CREATE TABLE IF NOT EXISTS education_goals (
                                id integer PRIMARY KEY,
                                user_id integer NOT NULL,
                                goal_title text,
                                goal_description text,
                                goal_category text,
                                status text,
                                progress_percentage integer,
                                created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (user_id) REFERENCES users (id)
                            );"""

    sql_create_tasks_daily_table = """CREATE TABLE IF NOT EXISTS tasks_daily (
                                id integer PRIMARY KEY,
                                user_id integer NOT NULL,
                                date text NOT NULL,
                                task_title text,
                                task_description text,
                                completed boolean,
                                priority integer,
                                FOREIGN KEY (user_id) REFERENCES users (id)
                            );"""

    sql_create_projects_table = """CREATE TABLE IF NOT EXISTS projects (
                                id integer PRIMARY KEY,
                                user_id integer NOT NULL,
                                project_name text,
                                project_description text,
                                progress_percentage integer,
                                status text,
                                created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (user_id) REFERENCES users (id)
                            );"""

    sql_create_financial_transactions_table = """CREATE TABLE IF NOT EXISTS financial_transactions (
                                id integer PRIMARY KEY,
                                user_id integer NOT NULL,
                                transaction_date text NOT NULL,
                                transaction_type text,
                                category text,
                                amount real,
                                notes text,
                                FOREIGN KEY (user_id) REFERENCES users (id)
                            );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create users table
        create_table(conn, sql_create_users_table)
        # create daily_logs table
        create_table(conn, sql_create_daily_logs_table)
        # create cognitive_games_sessions table
        create_table(conn, sql_create_cognitive_games_sessions_table)
        # create french_practice_sessions table
        create_table(conn, sql_create_french_practice_sessions_table)
        # create news_reading_sessions table
        create_table(conn, sql_create_news_reading_sessions_table)
        # create education_goals table
        create_table(conn, sql_create_education_goals_table)
        # create tasks_daily table
        create_table(conn, sql_create_tasks_daily_table)
        # create projects table
        create_table(conn, sql_create_projects_table)
        # create financial_transactions table
        create_table(conn, sql_create_financial_transactions_table)

        conn.close()
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()