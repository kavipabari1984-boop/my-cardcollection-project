import sqlite3
import pandas as pd

DB_NAME = "collector_app.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS master_checklist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            set_name TEXT NOT NULL,
            card_number TEXT NOT NULL,
            card_name TEXT NOT NULL,
            market_price REAL DEFAULT 0.0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            master_id INTEGER NOT NULL,
            condition TEXT NOT NULL,
            purchase_price REAL DEFAULT 0.0,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (master_id) REFERENCES master_checklist (id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

def add_master_card(set_name, card_number, card_name, market_price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO master_checklist (set_name, card_number, card_name, market_price) VALUES (?, ?, ?, ?)", 
                   (set_name, card_number, card_name, market_price))
    conn.commit()
    conn.close()

def add_to_inventory(master_id, condition, purchase_price, quantity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (master_id, condition, purchase_price, quantity) VALUES (?, ?, ?, ?)", 
                   (master_id, condition, purchase_price, quantity))
    conn.commit()
    conn.close()

def update_inventory_item(inventory_id, condition, purchase_price, quantity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET condition = ?, purchase_price = ?, quantity = ? WHERE id = ?", 
                   (condition, purchase_price, quantity, inventory_id))
    conn.commit()
    conn.close()

def update_market_price(master_id, new_price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE master_checklist SET market_price = ? WHERE id = ?", (new_price, master_id))
    conn.commit()
    conn.close()

def remove_from_inventory(inventory_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE id = ?", (inventory_id,))
    conn.commit()
    conn.close()

def remove_master_card(master_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM master_checklist WHERE id = ?", (master_id,))
    conn.commit()
    conn.close()

def get_master_df():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM master_checklist", conn)
    conn.close()
    return df

def get_inventory_df():
    conn = get_connection()
    query = """
        SELECT T1.id as inventory_id, T2.id as master_id, T2.set_name, 
               T2.card_number, T2.card_name, T1.condition, 
               T1.purchase_price, T1.quantity, T2.market_price
        FROM inventory T1
        JOIN master_checklist T2 ON T1.master_id = T2.id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_portfolio_summary():
    df = get_inventory_df()
    if df.empty:
        return {"total_cards": 0, "total_spent": 0.0, "market_value": 0.0, "profit_loss": 0.0}
    
    df['total_cost'] = df['purchase_price'] * df['quantity']
    df['total_value'] = df['market_price'] * df['quantity']
    
    total_spent = df['total_cost'].sum()
    market_value = df['total_value'].sum()
    
    return {
        "total_cards": int(df['quantity'].sum()),
        "total_spent": round(total_spent, 2),
        "market_value": round(market_value, 2),
        "profit_loss": round(market_value - total_spent, 2)
    }