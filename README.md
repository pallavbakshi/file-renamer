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

## Future Plans
- If user re-runs the script multiple times, revert loses the original file names. Need to fix this.
- Add auto-renaming feature. This will automatically open the file and find a suitable name for the file based on the content of the file. This will use LLM (Language Model) to find the most suitable name for the file.
- Add a feature to ignore some conventions. For example, if you don't want to change the case of the file name, you can use the `--ignore_case` flag.
- Sometimes changing file names can corrupt the file. Need to add a feature `--safe` that will create a copy of the file (or the folder) and rename the copy. This will ensure that the original file is not corrupted.
- Add a feature to rename files in the nested folders. Currently, it only renames files in the given folder (not in the sub-folders).