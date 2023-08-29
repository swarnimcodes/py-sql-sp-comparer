import os
import pandas as pd
import filecmp

# Define the base directory and source/test directories
base_dir = "C:\\Users\\swarn\\github\\Stored SPs"
source_dir = os.path.join(base_dir, "DB_PRMITR_ERP_20230701")
test_dirs = [
    os.path.join(base_dir, "DB_PRMITR_ERP_20230615_TEST_1"),
    os.path.join(base_dir, "DB_PRMITR_ERP_20230615_TEST_2"),
    os.path.join(base_dir, "DB_PRMITR_ERP_20230615_TEST_3")
]

# Create a list to store the data for each SP
sp_data = []

# Get the list of SQL files in the source directory
source_sql_files = os.listdir(source_dir)

# Iterate through each SQL file in the source directory
for sql_file in source_sql_files:
    sp_name = sql_file[:-4]  # Remove the ".sql" extension

    # Create a dictionary to store the presence in different test directories
    sp_info = {'SP Name': sp_name}

    source_sql_path = os.path.join(source_dir, sql_file)

    # Check presence in each test directory
    for test_dir in test_dirs:
        test_sql_path = os.path.join(test_dir, sql_file)
        if os.path.exists(test_sql_path):
            if filecmp.cmp(source_sql_path, test_sql_path):
                sp_info[os.path.basename(test_dir)] = 'present & equal'
            else:
                sp_info[os.path.basename(test_dir)] = 'present & unequal'
        else:
            sp_info[os.path.basename(test_dir)] = 'absent'

    sp_data.append(sp_info)

# Create a DataFrame from the collected data
df = pd.DataFrame(sp_data)

# Define the path for the output Excel file
output_excel_path = os.path.join(base_dir, 'SP_Presence_Report.xlsx')

# Write the DataFrame to an Excel file
df.to_excel(output_excel_path, index=False)
