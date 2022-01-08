# database.py

import sqlite3
from typing import List
import datetime
from model import ActionItem
conn = sqlite3.connect('action_items.db')
c = conn.cursor()


def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS action_items (
            task text,
            priority_level text,
            date_added text,
            date_completed text,
            status integer,
            position integer
            )""")


create_table()


def insert_action_item(action_item: ActionItem):
    c.execute('select count(*) FROM action_items')
    count = c.fetchone()[0]
    action_item.position = count if count else 0
    with conn:
        c.execute('INSERT INTO action_items VALUES (:task, :priority_level, :date_added, :date_completed, :status, :position)',
        {'task': action_item.task, 'priority_level': action_item.priority_level, 'date_added': action_item.date_added,
         'date_completed': action_item.date_completed, 'status': action_item.status, 'position': action_item.position})


def get_all_action_items() -> List[ActionItem]:
    c.execute('select * from action_items')
    results = c.fetchall()
    action_items = []
    for result in results:
        action_items.append(ActionItem(*result))
    return action_items


def delete_action_item(position):
    c.execute('select count(*) from action_items')
    count = c.fetchone()[0]

    with conn:
        c.execute("DELETE from action_items WHERE position=:position", {"position": position})
        for pos in range(position+1, count):
            change_position_(pos, pos-1, False)


def change_position(old_position: int, new_position: int, commit=True):
    c.execute('UPDATE action_items SET position = :position_new WHERE position = :position_old',
                {'position_old': old_position, 'position_new': new_position})
    if commit:
        conn.commit()


def update_action_item(position: int, task: str, priority_level: str):
    with conn:
        if task is not None and category is not None:
            c.execute('UPDATE action_items SET task = :task, priority_level = :priority_level WHERE position = :position',
                        {'position': position, 'task': task, 'priority_level': priority_level})
        elif task is not None:
            c.execute('UPDATE action_items SET task = :task WHERE position = :position',
                        {'position': position, 'task': task})
        elif priority_level is not None:
            c.execute('UPDATE action_items SET priority_level = :priority_level WHERE position = :position',
                        {'position': position, 'priority_level': priority_level})


def complete_action_item(position: int):
    c.execute('UPDATE action_items SET status = 2, date_completed = :date_completed WHERE position = :position',
                {'position': position, 'date_completed': datetime.datetime.now().isoformat()})
