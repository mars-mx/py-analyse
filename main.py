from __future__ import print_function, unicode_literals
import json
import re
import sys
import os

PATTERNS = None

RESULT = []

def analyse_pattern(line, pattern):
    return re.search(pattern, line)

def add_result(patternName, line, line_nr, context, context_line_nr, path):
    RESULT.append({
        "pattern": PATTERNS[patternName],
        "name": patternName,
        "line": line.strip().replace(";", ""),
        "line_nr": line_nr,
        "context": context.strip().replace(";", ""),
        "context_line_nr": context_line_nr,
        "path": path
    })

def find_context(content, idx):
    i = idx - 1
    while i >= 0:
        if re.search(r"^\s*class\s+\w+\s*:", content[i]) or re.search(r"^\s*def\s+\w+\s*\(.*\)\s*:", content[i]):
            return content[i].strip(), i
        i -= 1
    return "root", -1

def analyse_folder(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            analyse_file(os.path.join(root, file))
        for dir in dirs:
            analyse_folder(os.path.join(root, dir))

def analyse_file(path):
    print("Analyzing file: {}".format(path))
    with open(path, "r") as f:
        content = f.readlines()
    for idx, line in enumerate(content):
        for patternName in PATTERNS:
            regex_pattern = PATTERNS[patternName]["match"]
            if analyse_pattern(line, regex_pattern):
                context, context_line_nr = find_context(content, idx)
                add_result(patternName, line, idx + 1, context, context_line_nr, os.path.abspath(path))

def load_patterns(path):
    with open(path, "r") as f:
        return json.load(f)

def export_result(target):
    """
    Export the result to a csv file
    """
    with open(target, "w") as f:
        f.write("Name;Path;Line;Line Nr;Context;Context Line Nr;Description;Solution Available;Solution;Effort\n")
        for result in RESULT:
            f.write("{};{};{};{};{};{};{};{};{};{}\n".format(
                result['name'], result['path'], result['line'], result['line_nr'],
                result['context'], result['context_line_nr'], result['pattern']['description'],
                result['pattern']['solvable'], result['pattern']['solution'], result['pattern']['effort']
            ))

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
    export_result("result.csv")

if __name__ == "__main__":
    main()
