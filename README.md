# Python Proficiency
> A collection of python mini projects to practice implementing programming concepts and improve proficiency in the python programming language

## 🗃️ Projects
- 📁 [`File Organiser`](#-file-organiser)
- 📁 [`Text Analyser`](#-text-analyser)
- 📁 [`Web Scraper`](#-web-scraper)

### 📁 File Organiser
📄 [`file_organiser.py`](./file_organiser.py)

![file organiser command line interface running in the terminal](<media/file organiser demo.gif>)
#### Documentation
| Method | Description | Parameters | Returns |
|---|---|---|---|
| `files_to_move` | scans the directory and counts number of files to be organised |`path: str` - Path of the directory to be organised<hr>`group_folders: bool` - Flag that determines whether directories are also counted | `int` - number of files to be organised |
| `ignore` | determines whether a file should be ignored or not based on its type |`file: str` - filename<hr>`extension: str` - file extension | `bool` - `True` if the file should be ignored, else `False` |
| `get_path` | gets the path of the directory to be organised either as a command line argument or via an in-built CLI | `None` | `tuple[str, bool, bool]` - <br>[<br>path of directory to be organised<hr>flag that determines whether all sorted files are put in a single parent folder<hr>flag that determines whether pre-existing folders are put in a single parent folder<br>] |
| `create_dirs` | creates all folders required for sorting in chosen directory |`path: str` - parent directory to make folders in<hr>`group_sorted: bool` - flag that determines whether all sorted files are put in a single parent folder<hr>`group_folders: bool` - flag that determines whether pre-existing folders are put in a single parent folder<br> | `tuple[pathlib.Path, pathlib.Path]` - <br>[<br> path to the parent directory where files should be moved <hr> path to the parent directory where folders should be moved if `group_folders` is `True`, else `None`<br>] |
| `sort_files` | moves all files and folders into their allocated folders depending on directory type, file type and flags |`base: str` - base directory<hr>`files_path: pathlib.Path` destination directory for files<hr>`folders_path: pathlib.Path \| None` destination directory for folders (if applicable)<hr>`progress: rich.progress.Progress` - progress bar object for CLI<hr>`task_id: rich.progress.TaskID` - ID for task (organising the directory) for progress bar rendering | `None` |
| `delete_folders` | deletes any empty folders in the parent directory |`path: str` - path of parent directory | `None` |


#### Usage
With command line arguments
```shell
py file_organiser.py -p <directory path> --group-sorted y --group-folders n
```
Using CLI
```
py file_organiser.py

Paste the path for the directory to organise: 📂 <path>
? Would you like to group sorted files together in one parent folder? Y/n
? Would you like to group pre-existing folders together in one parent folder? Y/n
```

If not all command line flags are used, the CLI will prompt you for the missing parameters :)

### 📁 Text Analyser
📄 [`mini_text_analyser.py`](./mini_text_analyser.py)

![mini text analyser command line interface running in the terminal](<media/mini text analyser demo.gif>)
#### Documentation
| Method | Description | Parameters | Returns |
|---|---|---|---|
| `get_txt_path` | Gets the path of the text file to be analysed either as a command line argument or via an in-built CLI | `None` | `str` - path of the text file |
| `open_text_file` | Opens the file for a given string path |`path: str` - the path for the file to be opened | `str` - a string containing the written contents of the opened file |
| `stopword_removal` | Removes all stopwords from a given string (e.g. a, in, and, to etc.) | `text_string: str` - input text | `str` - text with stopwords removed |
| `count_words` | Counts the total number of words in a string, and all occurrences of individual words | `text_string: str` - input text | `tuple[int, dict[str, int]]` - the total number of words, and the count of each individual word |
| `most_common_word` | Returns the word that most commonly occurred in the text |`word_count_dict: dict[str, int]` - all words in the text and their number of occurrences | `str` - the word with the most occurrences |
| `get_time_str` | Converts time in minutes to hours and minutes |`input_time: int` - the total time in minutes | `str` - time in hours and minutes as text |
| `estimated_reading_time` | Calculates the average read time for a piece of text for someone with a 200-300WPM read speed |`total_word_count: int` - the total number of words in the text | `str` - a string description of the approximate reading time for the input text |
#### Usage

With command line arguments
```
py mini_text_analyser.py <path to text file>
? Remove stopwords from text analysis? Y/n
```
Using CLI
```
py mini_text_analyser.py
Paste the path to the txt file to analyse: 📄 <path to text file>
? Remove stopwords from text analysis? Y/n
```

### 📁 Web Scraper
Courtesy of 🌐 [Books to scrape](https://books.toscrape.com)

📄 [`book_scraper.py`](./Book%20Vending%20Machine/book_vending_machine/book_scraper.py)
📄 [`inventory.py`](./Book%20Vending%20Machine/book_vending_machine/inventory.py)
📄 [`models.py`](./Book%20Vending%20Machine/book_vending_machine/models.py)
📄 [`main.py`](./Book%20Vending%20Machine/main.py)

![book vending machine web scraper command line interface running in the terminal](<media/book vending machine demo.gif>)

#### Documentation
#### [`book_scraper.py`](./Book%20Vending%20Machine/book_vending_machine/book_scraper.py)
---

`base_url` - URL of main site

`url` - URL to scrape data from

`books` - list of book objects


| Method | Description | Parameters | Returns |
|---|---|---|---|
| `__get_all_books_from_url` | Returns data from url | `None` | `list[BeautifulSoup.PageElement]` - all html_content returned from site |
| `__get_rating_from_tag` | Converts rating listed on website from `str` to `int` |`rating_tag: BeautifulSoup.Tag` - HTML tag containing the book's rating | `int` - book number rating |
| `__get_book_info` | Extracts book listing info from product page |`book: BeautifulSoup.PageElement` - article element from the homepage containing the book summary | `dict[str, Any]` - book metadata |
| `get_all_books` | Returns all scraped books as a list of `Book` objects | `None` | `list[Book]` - all scraped books from website |

#### [`inventory.py`](./Book%20Vending%20Machine/book_vending_machine/inventory.py)
---

`inventory` - list of all book objects

| Method | Description | Parameters | Returns |
|---|---|---|---|
| `_heading` | Returns the heading to be printed to the terminal | `None` | `rich.markdown.Markdown` - rich markdown object containing inventory heading |
| `_rating` | Constructs a formatted string based on the input rating |`rating: int` - book rating | `str` - star rating as a formatted string |
| `_get_stock` | Constructs a rich table to display the books in the inventory | `None` | `rich.table.Table` - rich table containing the books in the system's inventory and metadata |
| `_get_book_details` | Turns book metadata into printable markdown format |`book: Book` - book object to extract information from | `list[tuple[str, bool]]` - list of printable elements, and a flag to indicate whether they should be rendered using `rich.markdown` or not |
| `print_stock_and_details` | Prints the details of a specific book to the terminal |`console: rich.console.Console` - the console object to print to | `None` |

#### [`models`](./Book%20Vending%20Machine/book_vending_machine/models.py)
```py
@dataclass
class Book():
    title: str
    description: str
    category: str
    rating: int
    price: float
    in_stock: bool
```