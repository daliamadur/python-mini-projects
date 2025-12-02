import argparse, nltk, math, json
from string import punctuation
from pprint import pprint
from nltk.corpus import stopwords
from InquirerPy import inquirer as iq
from pathlib import Path

def get_txt_path():
    #for parsing command-line arguments
    parser = argparse.ArgumentParser(description="Organise all files in a directory based on their type")

    #string path as argument (optional)
    parser.add_argument("path_string", nargs="?", help="(string) full path to txt file to analyse")
    #string path with --path or -p cli flags
    parser.add_argument("-p", "--path", help="(string) full path to txt file to analyse")

    args = parser.parse_args()

    #get cli argument input by the user
    try:
        if args:
            path_from_arg = args.path if args.path else args.path_string
        #prompt if no cli args
        path = path_from_arg if path_from_arg else input("Paste the path to the txt file to analyse: 📄 ").strip(" \" \'")
    except Exception as e:
        print(f"⚠️ Problem with opening file: {e}")
        
    
    #return path, group_sorted, group_folders flags
    return path

def open_text_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()
    
def stopword_removal(text_string):
    nltk.download('stopwords', quiet=True)

    words = [word.lower() for word in text_string.split()]
    stop_words = set(stopwords.words('english'))
    filtered = [word for word in words if word not in stop_words]

    return " ".join(filtered)

def count_words(text_string):
    word_dict = {}

    for word in text_string.split():
        cleaned_word = word.lower().strip(punctuation)

        if cleaned_word in word_dict:
            word_dict[cleaned_word] += 1
        else:
            word_dict[cleaned_word] = 1

    return len(text_string.split()), word_dict

def most_common_word(word_count_dict):
    most_common = "", 0

    for word, count in word_count_dict.items():
        if count > most_common[1]:
            most_common = word, count

    return most_common

def get_time_str(input_time):
    time_in_hours = int(input_time / 60 )

    if time_in_hours == 0:
        return f"{input_time % 60} {"minute" if input_time % 60 == 1 else "minutes"}"
    elif input_time%60 == 0:
        return f"{time_in_hours} {"hour" if time_in_hours == 1 else "hours"}"
    else:
        return f"{time_in_hours} {"hour" if time_in_hours == 1 else "hours"} and {input_time % 60} {"minute" if input_time % 60 == 1 else "minutes"}"

def estimated_reading_time(total_word_count):
    lb = math.floor(total_word_count / 300)
    ub = math.ceil(total_word_count / 200)

    reading_time = f"{lb} to {ub} minutes"

    if lb == ub:
        reading_time = f"{lb} minutes"
    
    if ub < 1:
        reading_time = "Less than a minute"
    
    if ub == 1:
        "Around 1 minute"
    
    if lb >= 60:
        f"{get_time_str(lb)} to {get_time_str(ub)}"    

    return reading_time

def main():
    path = get_txt_path()

    remove_stopwords = iq.confirm("Remove stopwords from text analysis?").execute()
    text_string = open_text_file(path)
    text_for_analysis = stopword_removal(text_string) if remove_stopwords else text_string

    total_word_count, _ = count_words(text_string)
    _, word_count = count_words(text_for_analysis)
    most_common = most_common_word(word_count)

    reading_time = estimated_reading_time(total_word_count)

    report = []

    report.append(f"Total word count: {total_word_count}")
    report.append(f"Most common word: \"{most_common[0]}\", occurs {most_common[1]} {"times" if most_common[1] != 1 else "time"}")
    report.append(f"Estimated reading time: {reading_time}")

    for line in report:
        print(line)

    print()
    print("Individual word count:")
    pprint(word_count, indent=2)

    create_report = iq.confirm("Generate analysis report?").execute()

    if create_report:
        parent_folder = Path(path).parent
        report_folder = parent_folder / f"\'{Path(path).stem}\' Analysis Report"
        json_path = report_folder / "Individual Word Count.json"
        report_path = report_folder / "Report.txt"
        report_folder.mkdir(exist_ok=True)

        try:
            with open(str(json_path), 'w') as json_file:
                json.dump(word_count, json_file, indent=4)

            with open(str(report_path), 'w') as report_file:
                report_file.writelines([f"{item}\n" for item in report])
        except Exception as e:
            print(f"⚠️ Problem with writing report: {e}")
        
        print("✅ Report created successfully")

main()