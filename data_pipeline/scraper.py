from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import pandas as pd


rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


book_data = []


for page in range(1, 6):

    url = f"https://books.toscrape.com/catalogue/page-{page}.html"

    response = requests.get(url)

    print("Page:", page)
    print("Status:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article")

    print("Books:", len(books))

    for book in books:

        title = book.find("h3").find("a")["title"]

        price = book.find("p", class_="price_color")
        price_text = price.text.strip()
        price_gbp = float(price_text.replace("Â£", ""))

        rating = book.find("p", class_="star-rating")
        rating_text = rating["class"][1]
        rating_value = rating_map[rating_text]

        availability = book.find("p", class_="instock availability")
        availability_text = availability.text.strip()
        in_stock = availability_text == "In stock"

        book_link = book.find("h3").find("a")["href"]

        book_url = urljoin(url, book_link)

        book_response = requests.get(book_url)

        book_soup = BeautifulSoup(book_response.text, "html.parser")

        breadcrumb = book_soup.find("ul", class_="breadcrumb")

        category = None

        if breadcrumb:

            categories = breadcrumb.find_all("li")

            if len(categories) >= 4:

                category = categories[2].text.strip()

                if category == "Add a comment":
                    category = None

        book_data.append({
            "title": title,
            "price_gbp": price_gbp,
            "rating": rating_value,
            "in_stock": in_stock,
            "category": category
        })


print("\nTotal books scraped:", len(book_data))


# Remove books where category could not be parsed

book_data = [
    book for book in book_data
    if book["category"] is not None
]


print("Books after removing category parse failures:", len(book_data))


# Convert to DataFrame

df = pd.DataFrame(book_data)


print("\nDataFrame information:")
print(df.info())


print("\nFirst 5 rows:")
print(df.head())


print("\nMissing values:")
print(df.isnull().sum())


print("\nUnknown categories:")
print((df["category"] == "Unknown").sum())


# Convert GBP to INR using the required fixed rate

df["price_inr"] = (df["price_gbp"] * 105.50).round(2)


print("\nFinal data:")
print(df.head())


# Save cleaned dataset

df.to_csv("data_pipeline/books_cleaned.csv", index=False)


print("\nDataset saved successfully.")