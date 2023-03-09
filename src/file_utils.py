import os


USER_ROOT_DIR = os.path.expanduser('~')
USER_PICTURES_DIR = os.path.join(USER_ROOT_DIR, 'Pictures')
USER_DOWNLOADS_DIR = os.path.join(USER_ROOT_DIR, 'Downloads')


def create_dirpath(dirpath: str) -> None:
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)


def sanitize_filename(filename: str) -> None:
    for ch in ['\\','/','<','>',':','\"','|','?','*']:
        if ch in filename:
            filename.replace(ch, '')


def resolve_duplicate_filenames(dir: str, filename: str):
    i = 1
    name, extension = os.path.splitext(filename)
    while os.path.exists(os.path.join(dir, filename)):
        filename = f'{name}({i}){extension}'
        i += 1
