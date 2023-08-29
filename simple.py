"""_summary_
1. check if the sql files have been modified after the corresponding html file
was generated

2. if the sql files have been modified -> regenerate the diff_html file

3. if the sql files have not been modified after the diff_html was generated,
on the next run do not generate the diff file. just exit.


"""
import os
import difflib
import sqlparse
import re

# sql_file_1 = "C:\\Users\\swarn\\github\\Stored SPs\\DB_PRMITR_ERP_20230615\\ACAD_TP_BRANCH_GET_DEGREE.sql"
# sql_file_2 = "C:\\Users\\swarn\\github\\Stored SPs\\DB_PRMITR_ERP_20230701\\ACAD_TP_BRANCH_GET_DEGREE.sql"
# diff_file = "C:\\Users\\swarn\\github\\py-sql-parse\\diffs\diiff_ACAD_TP_BRANCH_GET_DEGREE.sql_ACAD_TP_BRANCH_GET_DEGREE.sql.html"

"""_summary_
instead of passing a single file we need to pass a list of files and
attempt the same logic.
"""

source_db = os.listdir("C:\\Users\\swarn\\github\\Stored SPs\\DB_PRMITR_ERP_20230701")
test_db = os.listdir("C:\\Users\\swarn\\github\\Stored SPs\\DB_PRMITR_ERP_20230615")
diff_dir = "C:\\Users\\swarn\\github\\py-sql-parse\\simple_diffs"
source_db_dir = "C:\\Users\\swarn\\github\\Stored SPs\\DB_PRMITR_ERP_20230701"
test_db_dir = "C:\\Users\\swarn\\github\\Stored SPs\\DB_PRMITR_ERP_20230615"

def does_diff_exist(file_name) -> bool:
    diff_filename = "diff_" + file_name + ".html" #
    diff_file = os.path.join(diff_dir, diff_filename)
    # print(os.path.exists(diff_file))
    return os.path.exists(diff_file)

def sql_mod_after_diff(file_name__) -> bool:
    # diff_file = os.path.join(diff_dir, file_name__)
    if (does_diff_exist(file_name__) == True):
        diff_filename = "diff_" + file_name__ + ".html"
        time_modified_html = os.path.getmtime(os.path.join(diff_dir, diff_filename))
        print(os.path.join(diff_dir, file_name__))
        time_modified_sql_file_1 = os.path.getmtime(os.path.join(source_db_dir, file_name__))
        time_modified_sql_file_2 = os.path.getmtime(os.path.join(test_db_dir, file_name__))

        print(f"diff file was modified at: {time_modified_html}. sql files were modified at {time_modified_sql_file_1} and {time_modified_sql_file_2}")

        if (time_modified_html < time_modified_sql_file_1) or (time_modified_html < time_modified_sql_file_2):
            return True
        else:
            print("sql was not modified")
            return False
    else:
        print("diff file was not found")
        return True

def parse_sql(sql_filepath1, sql_filepath2) -> str:
    parsed_sql1 = sqlparse.parse(open(sql_filepath1, "r").read())
    # open(file2_path, 'r').read().upper()
    parsed_sql2 = sqlparse.parse(open(sql_filepath2, "r").read())
    diffed_html = generate_diff(open(sql_filepath1, "r").read(), open(sql_filepath2, "r").read())
    return diffed_html

"""_summary_
we need to generate diff only if differences exist....
"""

def do_differences_exist_in_sql(sql_path_1, sql_path_2):
    parsed_sql1_stringed = sqlparse.format(sql_path_1, reindent=True, keyword_case="upper")
    parsed_sql2_stringed = sqlparse.format(sql_path_2, reindent=True, keyword_case="upper")

    if (parsed_sql1_stringed == parsed_sql2_stringed):
        return False
    else:
        return True

def format_sql(sql_file_contents) -> str:
    stripped_sql_file = re.sub(r'--.*', '', sql_file_contents)
    stripped_sql_file = re.sub(r'/\*.*?\*/', '', stripped_sql_file, flags=re.DOTALL)
    stripped_sql_file = '\n'.join(' '.join(part.strip() for part in line.split() if part.strip()) for line in stripped_sql_file.splitlines() if line.strip())
    return stripped_sql_file


def generate_diff(parsed_sql1, parsed_sql2) -> str:
    # file1_formatted = sqlparse.format(file1_contents, reindent=True, keyword_case='upper', use_space_around_operators=True, indent_width=4).strip()
    parsed_sql1_stringed = sqlparse.format(parsed_sql1, reindent=True, keyword_case="upper")
    parsed_sql2_stringed = sqlparse.format(parsed_sql2, reindent=True, keyword_case="upper")

    stripped_sql_file_1 = format_sql(parsed_sql1_stringed)
    stripped_sql_file_2 = format_sql(parsed_sql2_stringed)
    if (stripped_sql_file_1 != stripped_sql_file_2):
        html_diff = difflib.HtmlDiff(tabsize=4, wrapcolumn=72).make_file(stripped_sql_file_1.splitlines(), stripped_sql_file_2.splitlines(), context=True, numlines=3)
        return html_diff
    else:
        print(f"No differences found between sql files")
        return "NO"

# def should_we_generate_diff(file_name) -> bool: #
#     if(does_diff_exist(file_name) == True and sql_mod_after_diff() == False):
#         print("no need to generate new diff")
#         return False
#     elif(does_diff_exist(file_name) == True and sql_mod_after_diff() == True):
#         return True
#         print("we need to generate new diff")
#     elif(does_diff_exist(file_name) == False and does_sql_file_exist_in_both(file_name) == False): #
#         print(f"{file_name} does not exist in Test DB, so diff need not be generated")
#         return False
#     elif(does_diff_exist(file_name) == True and does_sql_file_exist_in_both() == True and sql_mod_after_diff() == True):
#         print("we need to generate new diff because diff file doesnt exist")
#         return True

def should_we_generate_diff(file_name_from_main) -> bool:
    if (sql_mod_after_diff(file_name_from_main) == True):
        return True
    elif(do_differences_exist_in_sql(os.path.join(source_db_dir, file_name_from_main), os.path.join(test_db_dir, file_name_from_main)) == True):
        return True # should return false if no differences between sql files exist
    elif(do_differences_exist_in_sql(os.path.join(source_db_dir, file_name_from_main), os.path.join(test_db_dir, file_name_from_main)) == False):
        return False



# def does_sql_file_exist_in_both(sql_filename) -> bool:
#     if (sql_filename in source_db and sql_filename in test_db):
#         return True
#     elif (sql_filename not in test_db):
#         return False

def does_sql_file_exist_in_both(file_name_sql) -> bool:
    file1 = os.path.join(source_db_dir, file_name_sql)
    file2 = os.path.join(test_db_dir, file_name_sql)

    if (os.path.exists(file1) and os.path.exists(file2)):
        return True
    else:
        return False


def main() -> None:
    for file_name_ in source_db:
        if (does_sql_file_exist_in_both(file_name_)):
            # check if diff even exists
            to_generate_diff = should_we_generate_diff(file_name_)
            if (to_generate_diff == True):
                diffed_html = parse_sql(os.path.join(source_db_dir, file_name_), os.path.join(test_db_dir, file_name_))
                if (diffed_html != "NO"):
                    # write the diffed html to file
                    # diff_filename = os.path.join(diff_dir, "diff_", file_name, ".html")
                    diff_filename = "diff_" + file_name_ + ".html" #
                    output_path = os.path.join(diff_dir, diff_filename)
                    with open(output_path, 'w') as diff_file:
                        diff_file.write(diffed_html)
            else:
                print("to generate diff returned false")

        else:
            print(f"{file_name_} does not exist in {test_db_dir}")




if __name__ == "__main__":
    main()