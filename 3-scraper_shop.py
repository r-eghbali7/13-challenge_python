# bale -> parsaeghbali 
# address bot -> @python_learnbot

import requests
from bs4 import BeautifulSoup
import sqlite3


class ProductScraper:

    def __init__(self, db_name="products.db"):
        self.db_name = db_name
        self.create_table()

    # -------------------------
    # Create DB Table
    # -------------------------
    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                price TEXT
            )
        """)

        conn.commit()
        conn.close()

    # -------------------------
    # Fetch HTML
    # -------------------------
    def fetch_page(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.text
        else:
            print("❌ Error fetching page")
            return None

    # -------------------------
    # Parse Products
    # -------------------------
    def parse_products(self, html):

        soup = BeautifulSoup(html, "html.parser")

        products = []

        # این selector را باید با سایت واقعی تنظیم کنی
        items = soup.find_all("div", class_="product")

        for item in items:

            title = item.find("h2")

            price = item.find("span", class_="price")

            if title and price:

                products.append({
                    "title": title.text.strip(),
                    "price": price.text.strip()
                })

        return products

    # -------------------------
    # Save to SQLite
    # -------------------------
    def save_to_db(self, products):

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        for p in products:
            cursor.execute("""
                INSERT INTO products (title, price)
                VALUES (?, ?)
            """, (p["title"], p["price"]))

        conn.commit()
        conn.close()

        print(f"✅ Saved {len(products)} products")

    # -------------------------
    # Show Products
    # -------------------------
    def show_products(self):

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()

        print("\n📦 Products in DB:\n")

        for row in rows:
            print(f"{row[0]}. {row[1]} - {row[2]}")

        conn.close()


# -------------------------
# Main
# -------------------------
def main():

    scraper = ProductScraper()

    url = input("Enter shop URL: ")

    html = scraper.fetch_page(url)

    if html:
        products = scraper.parse_products(html)

        scraper.save_to_db(products)

        scraper.show_products()


if __name__ == "__main__":
    main()