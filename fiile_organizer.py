import os
import shutil
import re
import curses

# Core functions
def list_files(directory):
    """List files and folders in the directory."""
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def list_folders(directory):
    """List only folders in the directory."""
    return [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

def move_file(source, destination):
    """Move a file to a destination."""
    shutil.move(source, destination)

def rename_files(directory, pattern=None, replacement=None, append_text=None):
    """Rename files in a directory."""
    files = list_files(directory)
    for filename in files:
        old_path = os.path.join(directory, filename)
        if pattern and replacement:  # Regex-based renaming
            new_name = re.sub(pattern, replacement, filename)
        elif append_text:  # Append text
            name, ext = os.path.splitext(filename)
            new_name = name + append_text + ext
        else:
            continue
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)

# TUI functions
def tui(stdscr):
    """Text User Interface using curses."""
    curses.curs_set(0)
    current_dir = os.getcwd()
    selected_option = 0
    options = ["Relocate Files", "Rename All Files", "Partial Rename", "Exit"]

    while True:
        stdscr.clear()
        stdscr.addstr(f"Current Directory: {current_dir}\n", curses.color_pair(1))
        for idx, option in enumerate(options):
            if idx == selected_option:
                stdscr.addstr(f"> {option}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(f"  {option}\n")

        key = stdscr.getch()

        if key == curses.KEY_UP and selected_option > 0:
            selected_option -= 1
        elif key == curses.KEY_DOWN and selected_option < len(options) - 1:
            selected_option += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if options[selected_option] == "Exit":
                break
            elif options[selected_option] == "Relocate Files":
                stdscr.clear()
                stdscr.addstr("Enter source folder: ")
                stdscr.refresh()
                source = stdscr.getstr().decode('utf-8')

                stdscr.addstr("Enter destination folder: ")
                stdscr.refresh()
                destination = stdscr.getstr().decode('utf-8')

                try:
                    files = list_files(source)
                    for idx, file in enumerate(files):
                        stdscr.addstr(f"{idx + 1}. {file}\n")
                    stdscr.addstr("\nEnter file index to move: ")
                    stdscr.refresh()
                    idx_to_move = int(stdscr.getstr().decode('utf-8')) - 1

                    move_file(os.path.join(source, files[idx_to_move]), destination)
                    stdscr.addstr(f"File moved to {destination}\nPress any key to continue...")
                except Exception as e:
                    stdscr.addstr(f"Error: {e}\nPress any key to continue...")
                stdscr.getch()
            elif options[selected_option] == "Rename All Files":
                stdscr.clear()
                stdscr.addstr("Enter folder path: ")
                stdscr.refresh()
                folder = stdscr.getstr().decode('utf-8')

                stdscr.addstr("Enter text to append to all files: ")
                stdscr.refresh()
                append_text = stdscr.getstr().decode('utf-8')

                try:
                    rename_files(folder, append_text=append_text)
                    stdscr.addstr(f"Files renamed in {folder}\nPress any key to continue...")
                except Exception as e:
                    stdscr.addstr(f"Error: {e}\nPress any key to continue...")
                stdscr.getch()
            elif options[selected_option] == "Partial Rename":
                stdscr.clear()
                stdscr.addstr("Enter folder path: ")
                stdscr.refresh()
                folder = stdscr.getstr().decode('utf-8')

                stdscr.addstr("Enter regex pattern: ")
                stdscr.refresh()
                pattern = stdscr.getstr().decode('utf-8')

                stdscr.addstr("Enter replacement text: ")
                stdscr.refresh()
                replacement = stdscr.getstr().decode('utf-8')

                try:
                    rename_files(folder, pattern=pattern, replacement=replacement)
                    stdscr.addstr(f"Files renamed in {folder}\nPress any key to continue...")
                except Exception as e:
                    stdscr.addstr(f"Error: {e}\nPress any key to continue...")
                stdscr.getch()

curses.wrapper(tui)