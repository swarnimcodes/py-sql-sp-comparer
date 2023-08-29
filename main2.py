import nltk
import os
import difflib
import sqlparse
import re
import pandas as pd


output_dir = "diffs"


def strip_sql_comments(sql_file_contents):
    stripped_sql_file = re.sub(r'--.*', '', sql_file_contents)
    stripped_sql_file = re.sub(r'/\*.*?\*/', '', stripped_sql_file, flags=re.DOTALL)
    stripped_sql_file = '\n'.join(' '.join(part.strip() for part in line.split() if part.strip()) for line in stripped_sql_file.splitlines() if line.strip())
    return stripped_sql_file

def normalize_sql(file_contents): ## CHANGE
    file_contents = file_contents
    tokens = nltk.word_tokenize(file_contents)
    return tokens

# def generate_html_diff(file1_tokenized, file2_tokenized):
#     file1_reglued = "".join(file1_tokenized)
#     file2_reglued = "".join(file2_tokenized)
#     # file1_reglued_sql = sqlparse.format(sqlparse.parse(file1_reglued), keyword_case="upper", reindent=True, wrap_after=72)
#     html_diff = difflib.HtmlDiff(tabsize=4, wrapcolumn=72).make_file(file1_reglued.splitlines(), file2_reglued.splitlines(), context=True, numlines=3, charset='utf-8')
#     print(type(html_diff))
#     return html_diff

def generate_html_diff(file1_contents, file2_contents):
    file1_formatted = sqlparse.format(file1_contents, reindent=True, keyword_case='upper', use_space_around_operators=True, indent_width=4)
    file2_formatted = sqlparse.format(file2_contents, reindent=True, keyword_case='upper', use_space_around_operators=True, indent_width=4)

    html_diff = difflib.HtmlDiff(tabsize=4, wrapcolumn=72).make_file(file1_formatted.splitlines(), file2_formatted.splitlines(), context=True, numlines=3, charset='utf-8')
    return html_diff




def main():
    folder1_path = r"C:\\Users\\swarn\\github\\Stored SPs\\DB_PRMITR_ERP_20230615"
    folder2_path = r"C:\\Users\\swarn\\github\\Stored SPs\\DB_PRMITR_ERP_20230701"

    for sql_file in os.listdir(folder1_path):
        if sql_file.endswith(".sql"):
            file1_path = os.path.join(folder1_path, sql_file)
            file2_path = os.path.join(folder2_path, sql_file)

            if os.path.exists(file2_path):  # Make sure the corresponding file exists in the second folder
                file1_contents = open(file1_path, 'r').read().upper()
                file1_nocomments = strip_sql_comments(file1_contents)
                normalized_sql_1 = normalize_sql(file1_nocomments)

                file2_contents = open(file2_path, 'r').read().upper()
                file2_nocomments = strip_sql_comments(file2_contents)
                normalized_sql_2 = normalize_sql(file2_nocomments)

                if normalized_sql_1 == normalized_sql_2:
                    print(f"Files {sql_file} are equal")
                else:
                    print(f"Files {sql_file} are unequal")
                    diff_html = generate_html_diff(file1_nocomments, file2_nocomments)
                    diff_filename = os.path.join(output_dir, f"diff_{sql_file}.html")
                    with open(diff_filename, "w") as diff_file:
                        diff_file.write(diff_html)
            else:
                print(f"Corresponding file not found for {sql_file} in the second folder")

if __name__ == "__main__":
    main()