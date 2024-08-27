import json
import re
import sys
import os

PATTERNS = None

def analyse_pattern(line: str, pattern: str):
    return re.search(pattern, line)

def find_context(content, idx) -> tuple:
    i = idx - 1
    while i >= 0:
        if re.search(r"^\s*class\s+\w+\s*:", content[i]) or re.search(r"^\s*def\s+\w+\s*\(.*\)\s*:", content[i]):
            return content[i].strip(), i
        i -= 1
    return "root", -1

def analyse_folder(path: str):
    for root, dirs, files in os.walk(path):
        for file in files:
            analyse_file(os.path.join(root, file))
        for dir in dirs:
            analyse_folder(os.path.join(root, dir))

def analyse_file(path: str):
    print(f"Analyzing file: {path}")
    with open(path, "r") as f:
        content = f.readlines()
    for idx, line in enumerate(content):
        for patternName in PATTERNS:
            regex_pattern = PATTERNS[patternName]["match"]
            if analyse_pattern(line, regex_pattern):
                context, context_line_nr = find_context(content, idx)
                print(f"Pattern {patternName} found in line: {idx+1} with context: {context} at line: {context_line_nr+1}")

def load_patterns(path: str):
    with open(path, "r") as f:
        return json.load(f)

def main():
    pattern_path = sys.argv[1]
    path = sys.argv[2]
    if not os.path.isfile(pattern_path):
        raise FileNotFoundError(pattern_path)
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    global PATTERNS
    PATTERNS = load_patterns(pattern_path)
    if os.path.isdir(path):
        analyse_folder(path)
    else:
        analyse_file(path)

if __name__ == "__main__":
    main()