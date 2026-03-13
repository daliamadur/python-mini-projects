# Python Proficiency
*💾 A collection of python mini projects to practice implementing programming concepts and improve proficiency in the python programming language*

## 🗃️ Projects
- 📁 [`File Organiser`](#-file-organiser)
- 📁 [`Text Analyser`](#-text-analyser)
- 📁 [`Web Scraper`](#-web-scraper)

### 📁 File Organiser
📄 [`file_organiser.py`](./file_organiser.py)
#### Documentation
| Method | Description | Parameters | Returns |
|---|---|---|---|
| `files_to_move` | scans the directory and counts number of files to be organised |`path: str` - Path of the directory to be organised<hr>`group_folders: bool` - Flag that determines whether directories are also counted | `int` - number of files to be organised |
| `ignore` | determines whether a file should be ignored or not based on its type |`file: str` - filename<hr>`extension: str` - file extension | `bool` - `True` if the file should be ignored, else `False` |
| `get_path` | gets the path of the directory to be organised either as a command line argument or via an in-built CLI | *no parameters* | `tuple[str, bool, bool]` - <br>[<br>path of directory to be organised<hr>flag that determines whether all sorted files are put in a single parent folder<hr>flag that determines whether pre-existing folders are put in a single parent folder<br>] |
| `create_dirs` | creates all folders required for sorting in chosen directory |`path: str` - parent directory to make folders in<hr>`group_sorted: bool` - flag that determines whether all sorted files are put in a single parent folder<hr>`group_folders: bool` - flag that determines whether pre-existing folders are put in a single parent folder<br> | `tuple[Path, Path]` - <br>[<br> path to the parent directory where files should be moved <hr> path to the parent directory where folders should be moved if `group_folders` is `True`, else `None`<br>] |
| `sort_files` | moves all files and folders into their allocated folders depending on directory type, file type and flags |`base: str` - base directory<hr>`files_path: Path` destination directory for files<hr>`folders_path: Path \| None` destination directory for folders (if applicable)<hr>`progress: Progress` - progress bar object for CLI<hr>`task_id: TaskID` - ID for task (organising the directory) for progress bar rendering | `None` |
| `delete_folders` | deletes any empty folders in the parent directory |`path: str` - path of parent directory | `None` |


#### Usage
```
terminal stuff using command line args
```
```
terminal stuff using CLI
```

### 📁 Text Analyser
📄 [`mini_text_analyser.py`](./mini_text_analyser.py)
#### Documentation
| Method | Description | Parameters | Returns |
|---|---|---|---|
| `method` | desc |`param: type` - desc<hr> | `return type` - desc |
#### Usage

### 📁 Web Scraper
📄 [`book_scraper.py`](./Book%20Vending%20Machine/book_vending_machine/book_scraper.py)
📄 [`inventory.py`](./Book%20Vending%20Machine/book_vending_machine/inventory.py)
📄 [`models.py`](./Book%20Vending%20Machine/book_vending_machine/models.py)
📄 [`main.py`](./Book%20Vending%20Machine/main.py)
#### Documentation
| Method | Description | Parameters | Returns |
|---|---|---|---|
| `method` | desc |`param: type` - desc<hr> | `return type` - desc |
#### Usage