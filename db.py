import sqlite3
from contextlib import contextmanager


CREATE_TASK_TABLE_SQL = '''
  CREATE TABLE IF NOT EXISTS task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    due_date DATE
  );
'''


INSERT_TASK_SQL = '''
    INSERT INTO task (name, description, due_date)
    VALUES (?, ?, ?);
'''


DELETE_TASK_SQL = '''
    DELETE FROM task WHERE id = ?;
'''


SELECT_TASKS_SQL = '''
    SELECT name, description, due_date
    FROM task
    ORDER BY id
    LIMIT ? OFFSET ?;
'''


SELECT_TASK_BY_IDX_SQL = '''
    SELECT * FROM task
    ORDER BY id
    LIMIT 1 OFFSET ?;
'''


SELECT_TASK_COUNT_SQL = '''
    SELECT COUNT(*) FROM task;
'''


@contextmanager
def begin():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute(CREATE_TASK_TABLE_SQL)
    yield cursor
    conn.commit()
    conn.close()


def insert_task(name, description, due_date):
    with begin() as cursor:
        cursor.execute(INSERT_TASK_SQL, (name, description, due_date))


def list_tasks(page, page_size):
    with begin() as cursor:
        return cursor.execute(SELECT_TASKS_SQL, (page_size, page * page_size)).fetchall()


def delete_task(idx):
    with begin() as cursor:
        task = cursor.execute(SELECT_TASK_BY_IDX_SQL, (int(idx),)).fetchone()
        if not task:
            return None
        cursor.execute(DELETE_TASK_SQL, (task[0],))
        return task[1:]


def get_page_count(page_size):
    with begin() as cursor:
        task_count = cursor.execute(SELECT_TASK_COUNT_SQL).fetchone()[0]
        return (task_count - 1) // page_size + 1
