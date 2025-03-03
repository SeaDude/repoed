#!/usr/bin/env python3
"""
A CLI tool that aggregates source files into a single markdown file.
Requirements:
 - Must be run from a git repository (i.e. a directory with a .git folder and a .gitignore file).
 - It creates an output markdown file (repoed.md) which includes:
    • A commit section: listing the last 3 commit messages (or a note if there are none).
    • A section for README.md – which is processed first.
         - If README.md exists (and is not ignored), its contents are added.
         - If not, a note (“- Does not exist”) is added.
    • Sections for all other source files (those not matching patterns in .gitignore) 
         – each section begins with an h3 header (### filename), then a new line and the content
           surrounded by triple backticks, and ends with a horizontal rule (---).
"""

import os
import sys
import subprocess
import fnmatch

def get_git_commits():
    """Return the last three commit messages as a list.
       If there are fewer than three, return those that exist.
       If no commits exist, return an empty list.
    """
    try:
        result = subprocess.run(
            ["git", "log", "-n", "3", "--pretty=%s"],
            capture_output=True,
            text=True,
            check=True
        )
        commits = result.stdout.strip().splitlines()
        return commits
    except subprocess.CalledProcessError:
        return []

def read_gitignore():
    """Read the .gitignore file and return a list of non-empty, non-comment lines."""
    patterns = []
    gitignore_file = ".gitignore"
    if os.path.exists(gitignore_file):
        with open(gitignore_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    return patterns

def is_ignored(file_path, ignore_patterns):
    """
    Determine if file_path should be ignored based on ignore_patterns.
    Handles:
      - Patterns starting with '/' for repository-root relative matching.
      - Patterns ending with '/' to denote directories.
      - Literal patterns (with no wildcards) where file_path either equals the pattern
        or begins with the pattern plus a separator (to cover directories).
      - Basic negative patterns starting with '!' where the last matching rule wins.
    """
    ignore = False
    for pattern in ignore_patterns:
        negative = False
        if pattern.startswith('!'):
            negative = True
            pattern = pattern[1:]
        # For repository-root relative patterns, remove the leading '/'
        if pattern.startswith('/'):
            pattern = pattern[1:]
        # Handle directory patterns (ending with '/')
        if pattern.endswith('/'):
            pat = pattern.rstrip('/')
            if file_path == pat or file_path.startswith(pat + os.sep):
                ignore = not negative
            continue
        # If the pattern is literal (no wildcards), check for an exact or directory match.
        if not any(char in pattern for char in "*?["):
            if file_path == pattern or file_path.startswith(pattern + os.sep):
                ignore = not negative
                continue
        # Fallback: use fnmatch on the full path and basename.
        if fnmatch.fnmatch(file_path, pattern) or fnmatch.fnmatch(os.path.basename(file_path), pattern):
            ignore = not negative
    return ignore

def gather_source_files(ignore_patterns, exclude_files):
    """
    Walk the current directory recursively (skipping .git) and return a list of
    files that do not match any ignore pattern and are not in the exclude_files set.
    """
    source_files = []
    for root, dirs, files in os.walk("."):
        if ".git" in dirs:
            dirs.remove(".git")
        for file in files:
            rel_path = os.path.join(root, file)
            if rel_path.startswith("./"):
                rel_path = rel_path[2:]
            if rel_path in exclude_files:
                continue
            if is_ignored(rel_path, ignore_patterns):
                continue
            source_files.append(rel_path)
    return source_files

def read_file_content(file_path):
    """Read and return the content of a file; if an error occurs, return an error message."""
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def main():
    # Ensure we are in a git repository.
    if not os.path.isdir(".git"):
        print("Error: .git directory not found in current directory.")
        sys.exit(1)
    if not os.path.exists(".gitignore"):
        print("Error: .gitignore file not found in current directory.")
        sys.exit(1)

    output_filename = "repoed.md"  # Aggregated markdown file.
    ignore_patterns = read_gitignore()
    commits = get_git_commits()

    with open(output_filename, "w") as outfile:
        # --- Commit Messages Section ---
        if commits:
            outfile.write("### Last Commits\n")
            for commit in commits:
                outfile.write(f"- {commit}\n")
        else:
            outfile.write("### Last Commits\n")
            outfile.write("- Not committed yet\n")
        outfile.write("\n")

        # --- Process README.md First ---
        readme_path = "README.md"
        outfile.write("### README.md\n")
        if os.path.exists(readme_path) and not is_ignored(readme_path, ignore_patterns):
            outfile.write("\n```\n")
            content = read_file_content(readme_path)
            outfile.write(content + "\n")
            outfile.write("```\n")
        else:
            outfile.write("\n- Does not exist\n")
        outfile.write("---\n\n")

        # --- Process All Other Source Files ---
        exclude_files = {readme_path, ".gitignore", output_filename}
        source_files = gather_source_files(ignore_patterns, exclude_files)
        source_files.sort()  # Ensure consistent order

        for file in source_files:
            outfile.write(f"### {file}\n")
            outfile.write("\n```\n")
            content = read_file_content(file)
            outfile.write(content + "\n")
            outfile.write("```\n")
            outfile.write("---\n\n")

    print(f"Aggregated markdown file created: {output_filename}")

if __name__ == "__main__":
    main()
