# pip install dirsync
# Link to official documentation "https://pypi.org/project/dirsync/"

from dirsync import sync
source_path = 'source-path'
target_path = 'target-path'

sync(source_path, target_path, 'sync')  # for syncing from source to target
sync(target_path, source_path, 'sync')  # for syncing from target to source
