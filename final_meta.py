import os
from collections import defaultdict

# ... (variable definitions)

# Function to get file metadata (size and last modified timestamp)
def get_file_metadata(file_path):
    try:
        file_stats = os.stat(file_path)
        return file_stats.st_size, file_stats.st_mtime
    except Exception as e:
        print(f"Error getting metadata for {file_path}: {e}")
        return None, None

def find_differing_sql_files(source_folder, target_folders):
    differing_files = defaultdict(set)

    source_files = {sql_file: get_file_metadata(os.path.join(source_folder, sql_file)) for sql_file in os.listdir(source_folder) if sql_file.endswith(".sql")}
    target_files = {target_folder: {sql_file: get_file_metadata(os.path.join(target_folder, sql_file)) for sql_file in os.listdir(target_folder) if sql_file.endswith(".sql")} for target_folder in target_folders}

    for sql_file, source_metadata in source_files.items():
        differing = False
        for target_folder, target_files_metadata in target_files.items():
            target_metadata = target_files_metadata.get(sql_file)
            if not target_metadata or source_metadata != target_metadata:
                differing = True
                differing_files[target_folder].add(sql_file)
        if differing:
            differing_files[source_folder].add(sql_file)

    return differing_files

def main():
    differing_files = find_differing_sql_files(source_folder_path, target_folder_paths)

    # Print or process the differing files information
    for folder, differing_sql_files in differing_files.items():
        print(f"Differing files in {folder}:")
        for sql_file in differing_sql_files:
            print(sql_file)

if __name__ == "__main__":
    main()
