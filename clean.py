import argparse
import os
import tree
from send2trash import send2trash

def main():
    MUSIC_FORMATS = ['mp3', 'flac', 'waw', 'm4a']
    yes = set(['yes','y', 'ye', ''])
    no = set(['no','n'])

    args = unparse_arguments(MUSIC_FORMATS)

    empty_dirs = find_folders_not_containing(args.path, MUSIC_FORMATS)
    for folder in empty_dirs:
        if args.tree:
            tree.tree(folder, '  ', True)
        else:
            print(folder)

    if empty_dirs:
        print("Do you want to delete listed directories? [yes/no]")
        choice = input().lower()

        if (choice in yes):
            print("Deleting dirs")
            delete_dirs(empty_dirs)
        else:
            print("You have canceled this action")
    else:
        print("Your music library is already clean")

def delete_dirs(dirs):
    for folder in dirs:
        send2trash(folder)

def find_folders_not_containing(folder, formats):
    os.chdir(folder)
    result = []
    ignore = []
    for root, dirs, files in os.walk('.'):
        if starts_with_in(root, ignore):
            continue

        empty = is_empty_file_tree(root, formats)
        if empty:
            result.append(root)
            ignore = ignore + merge_root_path(root, dirs)
    return result

def merge_root_path(root, dirs):
    result = []

    for folder in dirs:
        result.append(os.path.join(root, folder))

    return result


def starts_with_in(path, dirs):
    for folder in dirs:
        if path.startswith(folder):
            return True

    return False

def is_empty_file_tree(directory, formats):
    result = []
    for root, dirs, files in os.walk(directory):
        for directory in dirs:
            result.append(is_empty_file_tree(os.path.join(root, directory), formats))

        return is_dirs_empty(result) and not search_files(files, formats)

def is_dirs_empty(result_list):
    for directory in result_list:
        if directory == False:
            return False

    return True

def search_files(files, formats):
    for sfile in files:
        for sformat in formats:
            if sfile.lower().endswith(sformat.lower()):
                return True;

    return False;

def unparse_arguments(formats):
    desc = "Script that scans folders and remove folders that do not contain music.\nSupported music formats:\n"

    for sformat in formats:
        desc += "  " + sformat + "\n"

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('path', help='Path to music library')
    parser.add_argument('-t', '--tree', help='Prints file tree that will be deleted', action="store_true")
    return parser.parse_args()

if __name__ == '__main__':
    main()
