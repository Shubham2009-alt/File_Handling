# File Handling in Python

A small menu-driven command-line application for practicing Python file operations with `pathlib.Path`.

## Features

- **Create** a new empty text file without overwriting an existing file.
- **Read** and display a UTF-8 text file.
- **Rename** an existing file.
- **Append** text to the end of an existing file.
- **Overwrite** the contents of an existing file.
- **Delete** a file after an explicit confirmation.
- Reject blank file paths and handle common errors such as missing files, duplicate names, and permission problems.

## Requirements

- Python 3.10 or newer
- No third-party packages

## Run the program

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Run:

   ```bash
   python file_handling.py
   ```

   On systems where Python 3 is invoked as `python3`, use `python3 file_handling.py`.

4. Choose an operation from the displayed menu and enter the requested file path.

## Example

```text
=== File Handling Menu ===
1. Create a file
2. Read a file
3. Rename a file
4. Append to a file
5. Overwrite a file
6. Delete a file
7. Exit
```

Relative paths are resolved from the directory where the program is run. Absolute paths are also accepted. The program uses UTF-8 when reading and writing text.

## Important behavior

- **Create** refuses to replace a file that already exists.
- **Append** and **overwrite** operate on existing files; they do not silently create a missing target.
- **Overwrite** asks for confirmation because it replaces the current contents.
- **Delete** asks for confirmation before removing a file.
- The program operates on the paths you enter. Check a path carefully before confirming overwrite or deletion.

## Run the tests

The project includes unit tests using Python's built-in `unittest` framework. From the project root, run:

```bash
python -m unittest discover -s tests -v
```

## Automatic checks\n\nGitHub Actions runs the unit tests on Python 3.10 and 3.13 whenever code is pushed or a pull request is opened. You can also run the same tests locally using the command above.\n\n## Project structure

```text
File_Handling/
├── file_handling.py
├── tests/
│   └── test_file_handling.py
├── .gitignore
└── README.md
```

## Concepts practiced

- `pathlib.Path` and filesystem paths
- File modes and UTF-8 text I/O
- Functions, exception handling, and input validation
- Safe handling of destructive operations
- Unit testing with `unittest`

## License

No license has been specified for this repository. If you plan to share or reuse this project publicly, consider adding a license that matches your intentions.
