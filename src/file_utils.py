import os

USER_PICTURES_DIR = os.path.join(os.path.expanduser('~'), 'Pictures')

# Utility to create provided path directories 
def create_dir_path(dir_path: str) -> None:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

# Utility to remove invalid filename chars
def sanitize_filename(filename: str) -> None:
    for ch in ['\\','/','<','>',':','\"','|','?','*']:
        if ch in filename:
            filename.replace(ch, '')