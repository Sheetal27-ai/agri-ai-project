import os

# always gives project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_path(*args):
    return os.path.join(BASE_DIR, *args)
