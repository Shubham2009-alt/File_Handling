"""Menu-driven file operations using pathlib.

Run with: python file_handling.py
"""

from pathlib import Path


def _to_path(file_path: str | Path) -> Path:
    """Convert a string or Path to a user-expanded filesystem path."""
    return Path(file_path).expanduser()


def _require_file(file_path: str | Path) -> Path:
    """Return a path if it points to an existing regular file."""
    path = _to_path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"No such file: {path}")
    if not path.is_file():
        raise IsADirectoryError(f"Not a regular file: {path}")

    return path


def create_file(file_path: str | Path) -> Path:
    """Create a new empty file; never overwrite an existing path."""
    path = _to_path(file_path)
    path.touch(exist_ok=False)
    return path


def read_file(file_path: str | Path) -> str:
    """Read and return a UTF-8 text file."""
    path = _require_file(file_path)
    return path.read_text(encoding="utf-8")


def rename_file(source: str | Path, destination: str | Path) -> Path:
    """Rename a file without replacing an existing destination."""
    source_path = _require_file(source)
    destination_path = _to_path(destination)

    if destination_path.exists():
        raise FileExistsError(f"Destination already exists: {destination_path}")
    if destination_path.is_symlink():
        raise FileExistsError(f"Destination already exists: {destination_path}")
    if destination_path.parent != Path(".") and not destination_path.parent.exists():
        raise FileNotFoundError(
            f"Destination directory does not exist: {destination_path.parent}"
        )
    if destination_path.parent.exists() and not destination_path.parent.is_dir():
        raise NotADirectoryError(
            f"Destination parent is not a directory: {destination_path.parent}"
        )

    return source_path.rename(destination_path)


def append_to_file(file_path: str | Path, text: str) -> Path:
    """Append UTF-8 text to an existing file."""
    path = _require_file(file_path)
    with path.open("a", encoding="utf-8", newline="") as file:
        file.write(text)
    return path


def overwrite_file(file_path: str | Path, text: str) -> Path:
    """Replace the UTF-8 text in an existing file."""
    path = _require_file(file_path)
    path.write_text(text, encoding="utf-8")
    return path


def delete_file(file_path: str | Path) -> None:
    """Delete an existing file (the interactive menu asks for confirmation)."""
    path = _require_file(file_path)
    path.unlink()


def _confirm(prompt: str) -> bool:
    """Return True only when the user answers yes."""
    return input(f"{prompt} [y/N]: ").strip().lower() in {"y", "yes"}


def _show_menu() -> None:
    print(
        "\n=== File Handling Menu ===\n"
        "1. Create a file\n"
        "2. Read a file\n"
        "3. Rename a file\n"
        "4. Append to a file\n"
        "5. Overwrite a file\n"
        "6. Delete a file\n"
        "7. Exit"
    )


def main() -> None:
    """Run the interactive command-line menu."""
    actions = {
        "1": "create",
        "2": "read",
        "3": "rename",
        "4": "append",
        "5": "overwrite",
        "6": "delete",
    }

    while True:
        _show_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "7":
            print("Goodbye!")
            break
        if choice not in actions:
            print("Invalid option. Enter a number from 1 to 7.")
            continue

        try:
            action = actions[choice]

            if action == "create":
                path = create_file(input("Enter the new file path: ").strip())
                print(f"Created: {path}")

            elif action == "read":
                path = input("Enter the file path to read: ").strip()
                print("\n--- File contents ---")
                print(read_file(path), end="")
                print("\n--- End of file ---")

            elif action == "rename":
                source = input("Enter the current file path: ").strip()
                destination = input("Enter the new file path: ").strip()
                print(f"Renamed to: {rename_file(source, destination)}")

            elif action == "append":
                path = input("Enter the file path: ").strip()
                text = input("Enter the text to append: ")
                append_to_file(path, text)
                print(f"Text appended to: {path}")

            elif action == "overwrite":
                path = input("Enter the file path: ").strip()
                if not _confirm(f"This will replace all contents of {path}. Continue?"):
                    print("Overwrite cancelled.")
                    continue
                text = input("Enter the replacement text: ")
                overwrite_file(path, text)
                print(f"Contents overwritten: {path}")

            elif action == "delete":
                path = input("Enter the file path to delete: ").strip()
                if not _confirm(f"This will permanently delete {path}. Continue?"):
                    print("Deletion cancelled.")
                    continue
                delete_file(path)
                print(f"Deleted: {path}")

        except (OSError, UnicodeError, ValueError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram stopped.")
