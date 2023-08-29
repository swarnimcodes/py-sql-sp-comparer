import os
import difflib
import sqlparse
import re
import multiprocessing
from joblib import Parallel, delayed

source_db_dir = "C:\\Users\\swarn\\github\\Stored SPs\\DB_PRMITR_ERP_20230701"
test_db_dir = "C:\\Users\\swarn\\github\\Stored SPs\\DB_PRMITR_ERP_20230615"
diff_dir = "C:\\Users\\swarn\\github\\py-sql-parse\\simple_diffs"
source_db = os.listdir(source_db_dir)

def does_diff_exist(file_name) -> bool:
    diff_filename = "diff_" + file_name + ".html"
    diff_file = os.path.join(diff_dir, diff_filename)
    return os.path.exists(diff_file)

def sql_mod_after_diff(file_name__) -> bool:
    if does_diff_exist(file_name__):
        diff_filename = "diff_" + file_name__ + ".html"
        time_modified_html = os.path.getmtime(os.path.join(diff_dir, diff_filename))
        time_modified_sql_file_1 = os.path.getmtime(os.path.join(source_db_dir, file_name__))
        time_modified_sql_file_2 = os.path.getmtime(os.path.join(test_db_dir, file_name__))
        return time_modified_html < time_modified_sql_file_1 or time_modified_html < time_modified_sql_file_2
    else:
        return True

def parse_sql(sql_filepath1, sql_filepath2) -> str:
    sql1_contents = open(sql_filepath1, "r").read()
    sql2_contents = open(sql_filepath2, "r").read()

    parsed_sql1 = sqlparse.parse(sql1_contents)
    parsed_sql2 = sqlparse.parse(sql2_contents)

    return generate_diff(sql1_contents, sql2_contents)

def do_differences_exist_in_sql(parsed_sql1, parsed_sql2):
    return parsed_sql1 != parsed_sql2

def format_sql(sql_file_contents) -> str:
    stripped_sql_file = re.sub(r'--.*', '', sql_file_contents)
    stripped_sql_file = re.sub(r'/\*.*?\*/', '', stripped_sql_file, flags=re.DOTALL)
    stripped_sql_file = '\n'.join(' '.join(part.strip() for part in line.split() if part.strip()) for line in stripped_sql_file.splitlines() if line.strip())
    return stripped_sql_file

def generate_diff(sql1, sql2) -> str:
    parsed_sql1_stringed = sqlparse.format(sql1, reindent=True, keyword_case="upper")
    parsed_sql2_stringed = sqlparse.format(sql2, reindent=True, keyword_case="upper")

    stripped_sql_file_1 = format_sql(parsed_sql1_stringed)
    stripped_sql_file_2 = format_sql(parsed_sql2_stringed)

    if stripped_sql_file_1 != stripped_sql_file_2:
        html_diff = difflib.HtmlDiff(tabsize=4, wrapcolumn=72).make_file(stripped_sql_file_1.splitlines(), stripped_sql_file_2.splitlines(), context=True, numlines=3)
        return html_diff
    else:
        print(f"No differences found between sql files")
        return "NO"

def should_we_generate_diff(file_name_, parsed_sql1, parsed_sql2) -> bool:
    if sql_mod_after_diff(file_name_):
        return True
    elif do_differences_exist_in_sql(parsed_sql1, parsed_sql2):
        return True
    return False

def process_sql_file(file_name_):
    file_path_1 = os.path.join(source_db_dir, file_name_)
    file_path_2 = os.path.join(test_db_dir, file_name_)

    if does_sql_file_exist_in_both(file_name_):
        parsed_sql1 = sqlparse.parse(open(file_path_1, "r").read())
        parsed_sql2 = sqlparse.parse(open(file_path_2, "r").read())

        if should_we_generate_diff(file_name_, parsed_sql1, parsed_sql2):
            diffed_html = parse_sql(file_path_1, file_path_2)
            if diffed_html != "NO":
                diff_filename = "diff_" + file_name_ + ".html"
                output_path = os.path.join(diff_dir, diff_filename)
                with open(output_path, 'w') as diff_file:
                    diff_file.write(diffed_html)
                print(f"{diff_filename} generated.")
            else:
                print(f"No differences found in {file_name_}.")
        else:
            print(f"No need to generate diff for {file_name_}.")
    else:
        print(f"{file_name_} does not exist in {test_db_dir}.")

def does_sql_file_exist_in_both(file_name_sql) -> bool:
    file1 = os.path.join(source_db_dir, file_name_sql)
    file2 = os.path.join(test_db_dir, file_name_sql)
    return os.path.exists(file1) and os.path.exists(file2)

def main():
    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(
        delayed(process_sql_file)(file_name_)
        for file_name_ in source_db
    )

if __name__ == "__main__":
    main()
