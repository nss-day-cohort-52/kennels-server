import json
import sqlite3

from models.customers import Customer


def get_customer_by_email(email):
    with sqlite3.connect('./kennel.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select *
        from Customer
        where email = ?
        """, (email, ))

        customers = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], row['email'])
            customers.append(customer.__dict__)
    
        return json.dumps(customers)
