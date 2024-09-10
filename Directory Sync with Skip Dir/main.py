import shutil
import os

# Define the source and target directories
source_directory = "path/to/source/repo1"  # Update with the actual path
target_directory = "path/to/target/repo2"  # Update with the actual path

# Function to copy files from source to target directory, excluding Git-related files
def copy_files(source, target):
    for root, dirs, files in os.walk(source):
        # Exclude Git-related directories (e.g., .git)
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            source_file = os.path.join(root, file)
            target_file = source_file.replace(source, target, 1)
            
            # Create target directory if it doesn't exist
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            
            # Copy the file to the target directory
            shutil.copy2(source_file, target_file)

# Copy files from source to target directory
copy_files(source_directory, target_directory)


# import os
# import shutil

# source_path = 'source-path'
# target_path = 'target-path'

# # List of directories to skip during synchronization
# directories_to_skip = ['dir_to_skip_1', 'dir_to_skip_2']

# def custom_sync(source, target):
#     for item in os.listdir(source):
#         source_item = os.path.join(source, item)
#         target_item = os.path.join(target, item)

#         if os.path.isdir(source_item):
#             # Check if the directory should be skipped
#             if item in directories_to_skip:
#                 continue

#             # Recursively sync subdirectories
#             custom_sync(source_item, target_item)
#         else:
#             # Copy files
#             shutil.copy2(source_item, target_item)

# # Start the custom synchronization
# custom_sync(source_path, target_path)