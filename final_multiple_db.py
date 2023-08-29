import os
import difflib
import sqlparse
import re
import pandas as pd
import nltk
import hashlib

nltk.download('punkt')  # Download NLTK data (only required once)

output_dir = "diffs"
excel_output_file = "SP_Comparison.xlsx"

# Databases to compare
database_paths = [
    "C:\\Users\\swarn\\github\\Stored SPs\\comp\\source",
    "C:\\Users\\swarn\\github\\Stored SPs\\comp\\test1",
    "C:\\Users\\swarn\\github\\Stored SPs\\comp\\test2",
    "C:\\Users\\swarn\\github\\Stored SPs\\comp\\test3"
]


def strip_sql_comments(sql_file_contents) -> str:
    stripped_sql_file = re.sub(r'--.*', '', sql_file_contents)
    stripped_sql_file = re.sub(r'/\*.*?\*/', '', stripped_sql_file, flags=re.DOTALL)
    stripped_sql_file = '\n'.join(' '.join(part.strip() for part in line.split() if part.strip()) for line in stripped_sql_file.splitlines() if line.strip())
    return stripped_sql_file


def normalize_sql(file_contents):
    file_contents = file_contents
    tokens = nltk.word_tokenize(file_contents)
    return tokens


def generate_html_diff(file1_contents, file2_contents, folder1_path, folder2_path):
    folder1_name = os.path.basename(folder1_path)
    folder2_name = os.path.basename(folder2_path)
    file1_formatted = sqlparse.format(file1_contents, reindent=True, keyword_case='upper',
                                      use_space_around_operators=True, indent_width=4).strip()
    file2_formatted = sqlparse.format(file2_contents, reindent=True, keyword_case='upper',
                                      use_space_around_operators=True, indent_width=4).strip()

    html_diff = difflib.HtmlDiff(tabsize=4, wrapcolumn=72).make_file(file1_formatted.splitlines(),
                                                                     file2_formatted.splitlines(), context=True,
                                                                     numlines=3, charset='utf-8',
                                                                     fromdesc=folder1_name, todesc=folder2_name)
    return html_diff

# A dictionary to store cached hashes
hash_cache = {}

def get_file_hash(file_path):
    if file_path in hash_cache:
        return hash_cache[file_path]
    else:
        file_contents = open(file_path, 'r').read().upper()
        file_nocomments = strip_sql_comments(file_contents)
        normalized_sql = normalize_sql(file_nocomments)
        normalized_sql_str = ' '.join(normalized_sql)
        file_hash = hashlib.sha1(normalized_sql_str.encode()).hexdigest()
        hash_cache[file_path] = file_hash
        return file_hash


def main():
    comparison_results = []

    for sql_file in os.listdir(database_paths[0]):
        if sql_file.endswith(".sql"):
            sp_name = sql_file
            file_paths = [os.path.join(db_path, sql_file) for db_path in database_paths]

            file_hashes = [get_file_hash(file_path) for file_path in file_paths]

            if all(hash == file_hashes[0] for hash in file_hashes):
                content_comparison = "Equal"
                print(f"Files {sql_file} are equal")
            else:
                content_comparison = "Different"
                print(f"Files {sql_file} are unequal")
                diff_html = generate_html_diff(*[strip_sql_comments(open(file_path, 'r').read()) for file_path in file_paths],
                                               folder1_path=database_paths[0], folder2_path=database_paths[1])
                diff_filename = os.path.join(output_dir, f"diff_{sql_file}.html")
                with open(diff_filename, "w") as diff_file:
                    diff_file.write(diff_html)

            file_presence = ["Present" if os.path.exists(file_path) else "Missing" for file_path in file_paths]

            comparison_results.append([sp_name] + file_presence + [content_comparison])

    df = pd.DataFrame(comparison_results, columns=["SP Name"] + [os.path.basename(db_path) for db_path in database_paths] + ["Content Comparison"])
    df.to_excel(excel_output_file, index=False)


if __name__ == "__main__":
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    main()
