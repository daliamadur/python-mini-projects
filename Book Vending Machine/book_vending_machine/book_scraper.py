import requests, re
from bs4 import BeautifulSoup

class BookScraper():
    def __init__(self):
        self.base_url = "https://books.toscrape.com"
        self.url = f"{self.base_url}/catalogue"
        self.books = []

    def __get_all_books_from_url(self):
        response = requests.get(self.base_url)

        if response.status_code != 200:
            raise ConnectionError(response.status_code)
        
        results = []
        
        for i in range(1, 51):
            response = requests.get(f"{self.url}/page-{i}.html")

            html_content = BeautifulSoup(response.text, 'html.parser')
            books_on_page = html_content.find_all('article', class_='product_pod')
            
            results.extend(books_on_page)

            break

        return results
    
    def __get_rating_from_tag(self, rating_tag):
        #convert from string to int
        ratings = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5
        }
        #convert tag to string, split by space, get 3rd word (contains 'Number">'), get rid of tag characters, convert to lowercase
        rating = str(rating_tag).split()[2].strip('">').lower()

        #get int version of number using dict
        return ratings.get(rating)
    
    def __get_book_info(self, book):
        book_url = f"{self.url}/{book.h3.a["href"]}"

        response = requests.get(book_url)
        html_book_content = BeautifulSoup(response.text, 'html.parser')
        
        title = html_book_content.h1.get_text()
        
        desc_heading = html_book_content.find("div", id="product_description")
        description = desc_heading.find_next().find_next().get_text()

        breadcrumb = html_book_content.find("ul")
        li_items = breadcrumb.find_all('li')

        category = li_items[2].a.get_text()
        rating_tag = html_book_content.select_one('p[class*="star-rating"]')
        rating = self.__get_rating_from_tag(rating_tag)

        info_table_data = html_book_content.find_all("td")
        price = info_table_data[3].get_text()
        cleaned_price = float(price.split("£")[1])

        in_stock_data = info_table_data[5]
        in_stock = bool(re.search("In stock", str(in_stock_data)))

        print(title, description, category, rating, cleaned_price, in_stock, sep="\n")

        return {
            "title": title,
            "description": description,
            "category": category,
            "rating": rating,
            "price": cleaned_price,
            "in_stock": in_stock
        }
    
    def get_all_books(self):
        all_books = self.__get_all_books_from_url()
        
        for book in all_books:
            book_info = self.__get_book_info(book)
            book_object = Book(
                book_info.get("title"),
                book_info.get("description"),
                book_info.get("category"),
                book_info.get("rating"),
                book_info.get("price"),
                book_info.get("in_stock")
            )
            self.books.append(book_object)

        return self.books