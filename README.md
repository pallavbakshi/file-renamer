# file-renamer
Rename files in a folder

## What is this?
This is a simple script that renames files in a folder. It can be used to rename files in a folder to follow a particular set of conventions. 

## How to use?
- To rename all files in a folder
    - `python file_renamer.py --folder <folder_path>`
- To rename a single file
    - `python file_renamer.py --file <file_path>`

## What are the conventions?
- Replace all spaces with hyphen (-).
- Lowercase all letters.
- Remove all special characters except hyphen (-) and underscore (_).
- Remove multiples (double/tripple) hypens (--).

## How to ignore files?
- By default, all dotfiles are ignored.
- You can ignore files by using the `--ignore` flag.
    - `python file_renamer.py --folder <folder_path> --ignore <file_name>` 

## How to ignore file extensions?
- By default, all file extensions are considered.
- You can ignore file extensions by using the `--ignore_ext` flag.
    - `python file_renamer.py --folder <folder_path> --ignore_ext <file_extension>`

## How to revert the changes?
Sometimes you don't like the renaming and want to revert the changes. You can do that by using the `--revert` flag. 

Under the hood, the script creates a dotfile called `.file_renamer.csv` in the folder. This file contains the original file names and the renamed file names. When you use the `--revert` flag, the script reads this file and reverts the changes.