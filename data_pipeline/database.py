import sqlite3
import pandas as pd


df = pd.read_csv("data_pipeline/books_cleaned.csv")

conn = sqlite3.connect("data_pipeline/books.db")

cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price_gbp REAL,
    price_inr REAL,
    rating INTEGER,
    in_stock BOOLEAN,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
)
""")


categories = df["category"].unique()

for category in categories:
    cursor.execute(
        "INSERT OR IGNORE INTO categories (category_name) VALUES (?)",
        (category,)
    )


for _, row in df.iterrows():

    cursor.execute(
        """
        INSERT INTO books
        (title, price_gbp, price_inr, rating, in_stock, category_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            row["title"],
            row["price_gbp"],
            row["price_inr"],
            row["rating"],
            row["in_stock"],
            cursor.execute(
                "SELECT category_id FROM categories WHERE category_name = ?",
                (row["category"],)
            ).fetchone()[0]
        )
    )


conn.commit()

print("Database created successfully.")

print("\nCategories:")
print(pd.read_sql("SELECT * FROM categories", conn))

print("\nBooks:")
print(pd.read_sql("SELECT * FROM books LIMIT 5", conn))

conn.close()