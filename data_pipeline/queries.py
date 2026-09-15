import sqlite3
import pandas as pd
import os

os.makedirs("data_pipeline/query_outputs", exist_ok=True)


conn = sqlite3.connect("data_pipeline/books.db")


query1 = """
SELECT title, price_gbp, rating
FROM books
WHERE rating >= 4
"""


result1 = pd.read_sql(query1, conn)
result1.to_csv("data_pipeline/query_outputs/query1_output.csv", index=False)

print("Query 1:")
print(query1)

print("Output:")
print(result1)

query2 = """
SELECT title, price_gbp
FROM books
ORDER BY price_gbp DESC
LIMIT 5
"""

result2 = pd.read_sql(query2, conn)
result2.to_csv("data_pipeline/query_outputs/query2_output.csv", index=False)

print("\nQuery 2:")
print(query2)

print("Output:")
print(result2)

query3 = """
SELECT DISTINCT categories.category_name
FROM books
JOIN categories
ON books.category_id = categories.category_id
WHERE categories.category_name IN ('Fiction', 'Mystery', 'History')
"""

result3 = pd.read_sql(query3, conn)
result3.to_csv("data_pipeline/query_outputs/query3_output.csv", index=False)

print("\nQuery 3:")
print(query3)

print("Output:")
print(result3)

query4 = """
SELECT title, price_gbp
FROM books
WHERE price_gbp BETWEEN 20 AND 40
ORDER BY price_gbp
"""

result4 = pd.read_sql(query4, conn)
result4.to_csv("data_pipeline/query_outputs/query4_output.csv", index=False)

print("\nQuery 4:")
print(query4)

print("Output:")
print(result4)

query5 = """
SELECT books.title, books.rating, categories.category_name
FROM books
JOIN categories
ON books.category_id = categories.category_id
WHERE books.rating IN (4, 5)
ORDER BY books.rating DESC
"""

result5 = pd.read_sql(query5, conn)
result5.to_csv("data_pipeline/query_outputs/query5_output.csv", index=False)

print("\nQuery 5:")
print(query5)

print("Output:")
print(result5)

# Reproduce JOIN using pandas merge

books_df = pd.read_sql(
    "SELECT book_id, title, rating, category_id FROM books",
    conn
)

categories_df = pd.read_sql(
    "SELECT category_id, category_name FROM categories",
    conn
)

merged_df = pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner"
)

merge_result = merged_df[
    merged_df["rating"].isin([4, 5])
][["title", "rating", "category_name"]].sort_values(
    "rating",
    ascending=False
)

print("\nPandas merge result:")
print(merge_result)

merge_result.to_csv(
    "data_pipeline/query_outputs/pandas_merge_output.csv",
    index=False
)

conn.close()

