import sys
import os

PATTERNS = 

def analyse_folder(path: str):
    pass

def analyse_file(path: str):
    pass

def main():
    pattern_path = sys.argv[1]
    path = sys.argv[2]
    if not os.path.isfile(pattern_path):
        raise FileNotFoundError(pattern_path)
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    if os.path.isdir(path):
        analyse_folder(path)
    else:
        analyse_file(path)

if __name__ == "__main__":
    main()