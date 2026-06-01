from rich.table import Table
from rich.markdown import Markdown
from rich.console import Console
from .models import Book
from InquirerPy import inquirer as q
import random

class Inventory():
    def __init__(self, inventory: list[Book]):
        self.inventory = inventory

    def _heading(self):
        return Markdown("# 📖 Example Stock 📖")

    def _rating(self, rating):
        return f"{"[#DBB331] ★ [/#DBB331]" * rating}{"[#3E3E3E] ☆ [/#3E3E3E]" * (5 - rating)}"

    def _get_stock(self):
        table = Table(show_header=True, header_style="bold #7B1F3B")

        table.add_column("Title", style="bold")
        table.add_column("Category", style="#717171")
        table.add_column("Rating", justify="center")
        table.add_column("Price", justify="center")
        table.add_column("In stock", justify="center")

        for book in self.inventory:
            table.add_row(book.title,
                            book.category,
                            self._rating(book.rating),
                            f"[bold #4F9E52]£{book.price:.2f}[/bold #4F9E52]",
                            "🗸" if book.in_stock else "[bold red]Not in stock[/bold red]")
            
        return table

    def _get_book_details(self, book: Book):
        details = [
            (f"## {book.title}", True),
            (f"🪙 **£{book.price:.2f}**", True),
            (f"🔖 **{book.category}**", True),
            ("[green]In Stock 🗸[/green]" if book.in_stock else "[dim]Not in stock[dim]", False),
            (f"{self._rating(book.rating)}", False),
            (f"> {book.description[:-8]}", True)
        ]
        
        return details

    def print_stock_and_details(self, console: Console):
        console.print(self._heading())
        console.print(self._get_stock())
        print_details = q.confirm("Would you like more stock details?").execute()
        
        last = None
        while print_details:
            book_list_menu = [{"value": book, "name": book.title} for book in self.inventory]
            book_list_menu.append({"value": None, "name": "Exit"})
                
            book = q.select(message= "Choose a book to view details", choices=book_list_menu, qmark="📚", amark=random.choice(["📕","📗","📘","📙"]), default=last if last else book_list_menu[0]).execute()

            if book is None:
                exit()
            else:
                for detail in self._get_book_details(book):
                    detail, md = detail
                    console.print(Markdown(detail) if md else detail)
                print()
                last = book