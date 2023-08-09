import os
import shutil
import hashlib
import time

# Path to the source file
paths = [{'source': 'source-file', 'dest': 'target-file'},
         {'source': 'source-file', 'dest': 'target-file'}]


def calculate_sha1(file_path):
    """Calculate the SHA-1 hash of a file."""
    sha1_hash = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha1_hash.update(chunk)
    return sha1_hash.hexdigest()


def synchronize_files(source_file, destination_file):
    """Synchronize source file to the destination file if changes are detected."""
    source_hash = calculate_sha1(source_file)
    destination_hash = calculate_sha1(destination_file)

    if source_hash != destination_hash:
        shutil.copy2(source_file, destination_file)
        print(f"Synchronized: {source_file} -> {destination_file}")
    else:
        print("No changes detected.")


if __name__ == '__main__':
    try:
        while True:
            for path in paths:
                synchronize_files(path['source'], path['dest'])
            time.sleep(5)  # Adjust the interval as needed
    except KeyboardInterrupt:
        print("Synchronization stopped.")
