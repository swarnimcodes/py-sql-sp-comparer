import nltk
import os
import difflib
import sqlparse
import re
import pandas as pd


output_dir = "diffs_PHINMA"
excel_output_file = "SP_Comparison_PHINMA_works2.xlsx"

# output_dir = "diffs"
# excel_output_file = "SP_Comparison.xlsx"

# Source Database
folder1_path = r"C:\\Users\\swarn\\Downloads\\PHINMA UAT\\SJC"

# Database to compare with source
folder2_path = r"C:\\Users\\swarn\\Downloads\\PHINMA UAT\\HK"


def strip_sql_comments(sql_file_contents) -> str:
    # Remove single-line comments (--)
    stripped_sql_file = re.sub(r'--.*', '', sql_file_contents)
    # Remove multi-line comments (/* */)
    stripped_sql_file = re.sub(r'/\*.*?\*/', '', stripped_sql_file, flags=re.DOTALL)
    # Remove extra whitespace and newlines at the beginning and end of lines
    stripped_sql_file = '\n'.join(line.strip() for line in stripped_sql_file.splitlines())
    return stripped_sql_file

# def normalize_sql(file_contents): ## CHANGE
#     file_contents = file_contents
#     tokens = nltk.word_tokenize(file_contents)
#     file_contents_stringed = ''.join(tokens)
#     return file_contents_stringed

def normalize_sql(file_contents):
    return file_contents


# def generate_html_diff(file1_tokenized, file2_tokenized):
#     file1_reglued = "".join(file1_tokenized)
#     file2_reglued = "".join(file2_tokenized)
#     # file1_reglued_sql = sqlparse.format(sqlparse.parse(file1_reglued), keyword_case="upper", reindent=True, wrap_after=72)
#     html_diff = difflib.HtmlDiff(tabsize=4, wrapcolumn=72).make_file(file1_reglued.splitlines(), file2_reglued.splitlines(), context=True, numlines=3, charset='utf-8')
#     print(type(html_diff))
#     return html_diff

# def generate_html_diff(file1_contents, file2_contents, folder1_path, folder2_path):
#     folder1_name = os.path.basename(folder1_path)
#     folder2_name = os.path.basename(folder2_path)
#     file1_formatted = sqlparse.format(file1_contents, reindent=False, keyword_case='upper', use_space_around_operators=False)
#     file2_formatted = sqlparse.format(file2_contents, reindent=False, keyword_case='upper', use_space_around_operators=False)

#     html_diff = difflib.HtmlDiff(tabsize=4, wrapcolumn=72).make_file(file1_formatted.splitlines(), file2_formatted.splitlines(), context=True, numlines=3, fromdesc=folder1_name, todesc=folder2_name)
#     return html_diff

def generate_html_diff(file1_contents, file2_contents, folder1_path, folder2_path):
    folder1_name = os.path.basename(folder1_path)
    folder2_name = os.path.basename(folder2_path)
    file1_formatted = sqlparse.format(file1_contents, reindent=False, keyword_case='upper', use_space_around_operators=True)
    file2_formatted = sqlparse.format(file2_contents, reindent=False, keyword_case='upper', use_space_around_operators=True)

    html_diff = difflib.HtmlDiff(tabsize=4, wrapcolumn=72).make_file(file1_formatted.splitlines(), file2_formatted.splitlines(), context=True, numlines=3, fromdesc=folder1_name, todesc=folder2_name)
    return html_diff




def main():
    comparison_results = []

    for sql_file in os.listdir(folder1_path): # Path of source will be passed here
        if sql_file.endswith(".sql"):
            file1_path = os.path.join(folder1_path, sql_file)
            file2_path = os.path.join(folder2_path, sql_file)

            sp_name = sql_file

            present_in_folder1 = os.path.exists(file1_path)
            present_in_folder2 = os.path.exists(file2_path)
            content_comparison = ""
            diff_file = ""

            if present_in_folder1 and present_in_folder2:
                file1_contents = open(file1_path, 'r').read()
                normalized_sql_1 = normalize_sql(file1_contents)
                file1_nocomments = strip_sql_comments(normalized_sql_1)

                file2_contents = open(file2_path, 'r').read()
                normalized_sql_2 = normalize_sql(file2_contents)
                file2_nocomments = strip_sql_comments(normalized_sql_2)

                if file1_nocomments == file2_nocomments:
                    content_comparison = "Equal"
                    print(f"Files {sql_file} are equal")
                else:
                    content_comparison = "Different"
                    print(f"Files {sql_file} are unequal")
                    diff_html = generate_html_diff(file1_contents, file2_contents, folder1_path, folder2_path)
                    diff_filename = os.path.join(output_dir, f"diff_{sql_file}.html")
                    with open(diff_filename, "w") as diff_file:
                        diff_file.write(diff_html)
                    diff_file = diff_filename
            else:
                content_comparison = "Missing in one of the folders"
                if not present_in_folder1:
                    diff_file = f"Missing in {folder1_path}"
                else:
                    diff_file = f"Missing in {folder2_path}"

            comparison_results.append([sp_name, present_in_folder1, present_in_folder2, content_comparison, diff_file])

    df = pd.DataFrame(comparison_results, columns=["SP Name", "Present in DB_PRMITR_ERP_20230615", "Present in DB_PRMITR_ERP_20230701", "Content Comparison", "Diff File"])
    df.to_excel(excel_output_file, index=False)

if __name__ == "__main__":
    main()