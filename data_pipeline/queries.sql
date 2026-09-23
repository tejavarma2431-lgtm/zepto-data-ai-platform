-- Query 1
SELECT title, price_gbp, rating
FROM books
WHERE rating >= 4;

-- Query 2
SELECT title, price_gbp
FROM books
ORDER BY price_gbp DESC
LIMIT 5;

-- Query 3
SELECT DISTINCT categories.category_name
FROM books
JOIN categories
ON books.category_id = categories.category_id
WHERE categories.category_name IN ('Fiction', 'Mystery', 'History');

-- Query 4
SELECT title, price_gbp
FROM books
WHERE price_gbp BETWEEN 20 AND 40
ORDER BY price_gbp;

-- Query 5
SELECT books.title, books.rating, categories.category_name
FROM books
JOIN categories
ON books.category_id = categories.category_id
WHERE books.rating IN (4, 5)
ORDER BY books.rating DESC;