import sqlite3
import json
from contextlib import contextmanager

DATABASE = 'orders.db'

def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                item_ids TEXT NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_at TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')
        conn.commit()

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def insert_order(order_id, user_id, item_ids, total_amount):
    try:
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO orders (order_id, user_id, item_ids, total_amount, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (order_id, user_id, json.dumps(item_ids), total_amount, 'pending'))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def get_order_status(order_id):
    with get_db_connection() as conn:
        row = conn.execute('SELECT status FROM orders WHERE order_id = ?', (order_id,)).fetchone()
        return row['status'] if row else None

def update_order_status(order_id, status):
    with get_db_connection() as conn:
        if status == 'processing':
            conn.execute('''
                UPDATE orders
                SET status = ?, started_at = CURRENT_TIMESTAMP
                WHERE order_id = ?
            ''', (status, order_id))
        elif status == 'completed':
            conn.execute('''
                UPDATE orders
                SET status = ?, completed_at = CURRENT_TIMESTAMP
                WHERE order_id = ?
            ''', (status, order_id))
        else:
            conn.execute('''
                UPDATE orders SET status = ? WHERE order_id = ?
            ''', (status, order_id))
        conn.commit()

def get_metrics():
    with get_db_connection() as conn:
        total = conn.execute('SELECT COUNT(*) AS total FROM orders').fetchone()['total']
        avg_time = conn.execute('''
            SELECT AVG(STRFTIME('%s', completed_at) - STRFTIME('%s', started_at)) AS avg
            FROM orders WHERE status = 'completed'
        ''').fetchone()['avg'] or 0
        status_counts = {row['status']: row['count'] for row in conn.execute('''
            SELECT status, COUNT(*) AS count FROM orders GROUP BY status
        ''')}
        return {
            'total_orders': total,
            'average_processing_time': avg_time,
            'status_counts': status_counts
        }