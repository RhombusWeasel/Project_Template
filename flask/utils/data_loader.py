import os
import json
from utils.db import init_db, save_data_to_db, load_data_from_db


def load_folder_to_db(db_name, table_name, folder_path):
    # Initialize the database
    init_db(db_name)

    # Recursively search for JSON files in the given directory
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                # remove the .json extension to get the tree_id
                tree_id = os.path.splitext(file)[0]
                file_path = os.path.join(root, file)

                # Check if the data already exists in the database
                if load_data_from_db(db_name, table_name, tree_id) is not None:
                    print(
                        f"Data for tree {tree_id} already exists in database. Skipping.")
                    continue

                # Load the data from the JSON file
                with open(file_path, 'r') as f:
                    data = json.load(f)

                # Save the data to the database
                save_data_to_db(db_name, table_name, tree_id, data)

                print(
                    f"Successfully added data for tree {tree_id} to database.")
