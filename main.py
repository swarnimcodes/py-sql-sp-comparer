import nltk
import os
import difflib
import sqlparse
import re

output_dir = "diffs"

def strip_sql_comments(sql_file_contents):
    # stripped_sql_file = sql_file_contents.format(sql_file.strip(), strip_comments=True)
    stripped_sql_file = re.sub(r'--.*', '', sql_file_contents)
    stripped_sql_file = re.sub(r'/\*.*?\*/', '', stripped_sql_file, flags=re.DOTALL)
    # stripped_sql_file = '\n'.join(line for line in stripped_sql_file.splitlines() if line.strip())  # Remove empty lines
    # Remove empty lines and convert double spaces to a single space
    stripped_sql_file = '\n'.join(' '.join(part.strip() for part in line.split() if part.strip()) for line in stripped_sql_file.splitlines() if line.strip())
    # print(stripped_sql_file)
    return stripped_sql_file

def normalize_sql(file_contents): ## CHANGE
    file_contents = file_contents.upper()
    tokens = nltk.word_tokenize(file_contents)
    return tokens

def generate_html_diff(file1_tokenized, file2_tokenized):
    file1_reglued = "".join(file1_tokenized)
    file2_reglued = "".join(file2_tokenized)
    html_diff = difflib.HtmlDiff(tabsize=4, wrapcolumn=72).make_file(file1_reglued.splitlines(), file2_reglued.splitlines(), context=True, numlines=3, charset='utf-8')
    print(type(html_diff))
    return html_diff




def main():
    sql_file_path1 = "C:\\Users\\swarn\\github\\Stored SPs\\DB_PRMITR_ERP_20230615\\PKG_REGIST_SP_REPORT_BULK_EXAM_HALLTICKET.sql"
    file1_contents = open(sql_file_path1, 'r').read()
    file1_nocomments = strip_sql_comments(file1_contents)
    normalized_sql_1 = normalize_sql(file1_nocomments) # Tokenize --> gives sql without space

    sql_file_path2 = "C:\\Users\\swarn\\github\\Stored SPs\\DB_PRMITR_ERP_20230701\\PKG_REGIST_SP_REPORT_BULK_EXAM_HALLTICKET.sql"
    file2_contents = open(sql_file_path2, 'r').read()
    file2_nocomments = strip_sql_comments(file2_contents)
    normalized_sql_2 = normalize_sql(file2_nocomments) # Tokenize --> gives sql without space



    if normalized_sql_1 == normalized_sql_2:
        print("equal")
    else:
        print("unequal")
        diff_html = generate_html_diff(file1_nocomments, file2_nocomments)
        diff_filename = os.path.join(output_dir, "diff_file.html")
        with open(diff_filename, "w") as diff_file:
            diff_file.write(diff_html)

if __name__ == "__main__":
    main()