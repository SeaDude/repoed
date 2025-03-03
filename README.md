# repoed

**repoed** is a Python CLI tool that aggregates source files from your git repository into a single markdown file. This aggregated document includes the last three commit messages and all your source code (filtered by your `.gitignore`) wrapped in fenced code blocks. By consolidating your entire codebase into one file, **repoed** helps you interact with large language models (LLMs) by providing complete in-context code for analysis, debugging, and discussion.

---

## **Features**

- **Automated Aggregation**
  - Generates an aggregated markdown file (`repoed.md`) from your repository.
  - Captures the last three git commit messages.
  - Processes `README.md` first, then all other source files.
- **Gitignore Compliance**
  - Respects your `.gitignore` rules to skip files and directories like `node_modules` or `.next`.
- **Fenced Code Blocks**
  - Wraps each source file's content in triple backticks for clean markdown formatting.
- **LLM-Enhanced Context**
  - Provides complete in-context source code to LLMs for more effective analysis and assistance.
- **Easy Integration**
  - Designed to be executable and symlinked to `~/.local/bin` for quick command-line access.

---

## **Prerequisites**

- **Python 3**  
  Ensure Python 3 is installed on your system.

---

## **Installation Steps**

1. **Clone the Repository** (e.g., to `~/projects/repoed`):
   ```bash
   git clone https://github.com/<your-github-handle>/repoed.git
   cd repoed
   ```

2. **Make the Script Executable**:
   ```bash
   chmod +x repoed
   ```

3. **Symlink to Your Local Bin Directory**:
   ```bash
   ln -s ~/projects/repoed/repoed ~/.local/bin/repoed
   ```
   - Ensure that `~/.local/bin` is in your PATH. If it isn’t, add the following line to your `~/.bashrc` or `~/.zshrc`:
     ```bash
     export PATH="$HOME/.local/bin:$PATH"
     ```
   - Reload your shell configuration:
     ```bash
     source ~/.bashrc
     ```

---

## **Usage**

Run `repoed` in the root directory of your git repository:
```bash
repoed
```
This command will create a file called `repoed.md` containing:
- **Commit Section:**  
  Displays the last three commit messages (or a note if no commits exist).
- **README.md Section:**  
  Shows the content of your `README.md` (wrapped in triple backticks) or a note if it does not exist.
- **Source File Sections:**  
  Lists all other source files (not ignored by `.gitignore`), each with:
  - An H3 header (`### filename`)
  - A new line followed by the file's content enclosed in triple backticks
  - A horizontal rule (`---`) to separate sections

---

## **Interact with LLMs**

**repoed** is designed to enhance your interactions with large language models. By providing all your source code in one context-rich markdown file, you can:
- Easily supply complete project context when asking for help.
- Receive more accurate and informed responses for code reviews, debugging, and feature suggestions.
- Save time by avoiding manual concatenation of source files when interfacing with LLMs.

---

## **Credits**

Developed interactively and in collaboration with OpenAI's GPT models, **repoed** streamlines the process of aggregating repository files into a single, well-formatted markdown document, making it easier to interact with LLMs.

**Initial prompt**:

```
Generate a simple CLI tool that meets the following requirements: 
1. Written in python
2. Stand-alone tool (for version control purposes) that will be:
    - Made executable (runs on Linux)
    - Symlinked from ~/projects/repoed to ~/.local/bin/repoed
3. When run in a terminal session, the tool will:
    - Look for a .git directory and a .gitignore file
    - Add all the source files NOT found in the .gitignore file into a SINGLE markdown file.
    - Each source file name becomes a new h3 header (###)
    - Each source file ends with a horizontal line (---)
    - The FIRST source file to include in the markdown file is the README.md.
    - If README.md does not yet exist, continue with the other files, noting 
        
        ```
        ### README.md
        - Does not exist
        ```

    - The H3 in the markdown file should be the last 3 commit messages from the .git directory. 
    - If there are not yet 3 commits, include which commits do exist. 
    - If no commits yet exist, continue finishing the markdown file, noting: 
    
      ```
      ### Last Commits
      - Not committed yet
      ```
```

---

## **License**

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
