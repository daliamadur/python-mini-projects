from book_vending_machine import BookScraper, Book, Inventory
import random
from rich.console import Console
from rich.theme import Theme

try:
    console = Console(
        theme=Theme({"markdown.block_quote": "dim"})
        )
    
    scraper = BookScraper()

    with console.status("Loading stock info and building inventory", spinner="aesthetic") as status:
        pass
        all_books: list[Book] = scraper.get_all_books()
        
        #grab 5 example books and print    
        example_inventory: list[Book] = random.sample(all_books, 5)

    inventory = Inventory(example_inventory)
    inventory.print_stock_and_details(console)

except Exception as e:
    print("Error:", e, e.__traceback__.tb_lineno)