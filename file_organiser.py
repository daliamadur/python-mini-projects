import shutil, argparse, time
from pathlib import Path
from rich.progress import Progress
from rich.console import Console
from InquirerPy import inquirer as iq

TYPES = {
    "Notes": {"txt", "rtf"},
    "Documents": {"docx", "doc", "wps", "wpd", "odt", "md", "ppt", "pptx", "odp", "pub"},
    "PDFs": {"pdf"},
    "Spreadsheets": {"csv", "xls", "xlsx", "ods"},
    "Images": {"jpg", "jpeg", "png", "webp", "gif", "tiff", "bmp", "eps", "svg"},
    "Audio": {"mp3", "wma", "snd", "wav", "ra", "au", "aac", "midi"},
    "Videos": {"mp4", "3gp", "avi", "mpg", "mov", "wmv"},
    "Archives": {"rar", "zip", "hqx", "7z", "gz", "tar"},
    "Scripts": {"py", "js", "ts", "sh", "bat", "ps1"}
}

SORTED_FILES = "Sorted Files"
SORTED_FOLDERS = "Sorted Folders"
MISC_FOLDER = "Misc"

ALL_FOLDERS = list(TYPES.keys()) + [SORTED_FILES, SORTED_FOLDERS, MISC_FOLDER]

class FileSortError(Exception):
    pass

def files_to_move(path, group_folders):
    num = 0
    directory = Path(path)

    #if not group folders -> continue else num += 1 for each file in dir
    for file in directory.iterdir():
        if (not group_folders and file.is_dir()) or file in ALL_FOLDERS:
            continue
        num += 1

    return num

def ignore(file, extension):
    IGNORED_FILES = {
        "desktop.ini",
        "Thumbs.db",
        ".DS_Store",
        "ehthumbs.db"
    }

    IGNORED_EXTENSIONS = {
        "ini",
        "db",
        "sys",
        "tmp",
        "lnk"
    }

    return file in IGNORED_FILES or extension in IGNORED_EXTENSIONS

def get_path():
    #for parsing command-line arguments
    parser = argparse.ArgumentParser(description="Organise all files in a directory based on their type")

    #string path as argument (optional)
    parser.add_argument("path_string", nargs="?", help="(string) full path to directory to organise")
    #string path with --path or -p cli flags
    parser.add_argument("-p", "--path", help="(string) full path to directory to organise")
    #group files
    parser.add_argument("--group-sorted", help="(y/n) will group all folders containing sorted files together in a single parent directory")
    #group folders
    parser.add_argument("--group-folders", help="(y/n) will group any pre-existing subdirectories together in a single parent directory")

    args = parser.parse_args()

    #get cli argument input by the user
    try:
        if args:
            path_from_arg = args.path if args.path else args.path_string
            group_sorted_from_arg = args.group_sorted
            group_folders_from_arg = args.group_folders
        #prompt if no cli args
        path = path_from_arg if path_from_arg else input("Paste the path for the directory to organise: 📂 ").strip(" \" \'")
        group_sorted = group_sorted_from_arg == 'y' if group_sorted_from_arg else iq.confirm("Would you like to group sorted files together in one parent folder?").execute()
        group_folders = group_folders_from_arg == 'y' if group_folders_from_arg else iq.confirm("Would you like to group pre-existing folders together in one parent folder?").execute()
    except Exception as e:
        print(f"Error with opening directory: {e}")
    
    #return path, group_sorted, group_folders flags
    return path, group_sorted, group_folders

def create_dirs(path, group_sorted, group_folders):
    base_path = Path(path)
    folders = list(TYPES.keys()) + [MISC_FOLDER]

    files_path = base_path / SORTED_FILES if group_sorted else base_path
    folders_path = base_path / SORTED_FOLDERS if group_folders else None

    if group_sorted:
        #make parent folder for sorted files
        files_path.mkdir(exist_ok=True)

    for folder in folders:
        #create new folders for each file type (or skip if already exists)
        new_folder = files_path / folder
        new_folder.mkdir(exist_ok=True)
        time.sleep(0.05)

    if group_folders:
        folders_path.mkdir(exist_ok=True)

    return files_path, folders_path

def sort_files(base, files_path, folders_path, progress, task_id):
    #get all files in directory
    base_path = Path(base)

    #move all directories (if flag)
    if folders_path:
        for dir_path in base_path.iterdir():
            folder = dir_path.name
            #put pre-existing folders in new parent folder if flag
            try:
                if dir_path.is_dir() and folder not in ALL_FOLDERS:
                    source = base_path / folder
                    destination = folders_path / folder
                
                    shutil.move(source, destination)
                    progress.update(task_id, advance=1)
                    time.sleep(0.05)
            except Exception as e:
                raise FileSortError(folder) from e
    
    for file_path in base_path.iterdir():
        file = file_path.name
        #check if item in directory is a file (skips folders)
        if not file_path.is_file():
            continue

        #path/file.ext
        source = file_path
        #get file extension
        extension = file_path.suffix.strip(".")

        #skip file if it's a system file
        if ignore(file, extension):
            continue
        
        #track whether file type is in dict
        type_exists = False

        for folder, extensions in TYPES.items():
            #check file's extension is in dict
            if extension in extensions:
                #set destination to corresponding folder
                destination = files_path / folder / file
                type_exists = True
                break

        if not type_exists:
            #put in misc folder if type isn't in dict
            destination = files_path / MISC_FOLDER / file

        try:
            #move the file to its desginated folder
            shutil.move(source, destination)
            progress.update(task_id, advance=1)
            time.sleep(0.05)
        except Exception as e:
            raise FileSortError(file) from e
                    
def delete_folders(path):
    base_path = Path(path)

    for folder in base_path.iterdir():
        if folder.is_dir() and not list(folder.iterdir()):
            folder.rmdir()
        time.sleep(0.05)

def main():
    try:
        path, group_sorted, group_folders = get_path()
        console = Console()

        thing_to_move = "files and folders" if group_folders else "files"

        total_files = files_to_move(path, group_folders)

        with console.status("📁 Scanning/Creating folders", spinner="dots"):
            files_path, folders_path = create_dirs(path, group_sorted, group_folders)
            console.print("✅ Folders created successfully", style="#56D18B")

        with Progress() as progress:
            sort_files_task = progress.add_task(f"🗃️ Moving {thing_to_move}...", total=total_files)
            
            sort_files(path, files_path, folders_path, progress, sort_files_task)

        with console.status("📂 Deleting empty folders", spinner="dots"):
            delete_folders(path)

        console.print("✅ All files successfully organised", style="#56D18B")


    except Exception as e:
        console.print(f"❗ A file caused an error", style="#F23450")
        console.print(f"⚠️ {e}", style="#FFB857")

main()