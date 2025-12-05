from book_vending_machine import Book, BookScraper, Inventory, Basket, PurchaseManager

try:
    scraper = BookScraper()
    all_books = scraper.get_all_books()
    inventory = Inventory(all_books)

    print(inventory.books)
except Exception as e:
    print("Error:", e, e.__traceback__.tb_lineno)