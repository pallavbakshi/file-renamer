import os
import re
import csv
import click
import shutil

from typing import Tuple


@click.command()
@click.option("--folder", help="The folder containing the files to rename.")
@click.option("--file", help="A single file to rename.")
@click.option(
    "--revert",
    is_flag=True,
    help="Revert the file names to their original state.",
)
@click.option(
    "--ignore",
    type=click.Path(exists=True),
    multiple=True,
    help="File path to ignore when renaming. You can give multiple file paths using --ignore <file_path> multiple times. Give complete file path.",
)
@click.option(
    "--ignore_ext",
    multiple=True,
    help="File extensions to ignore when renaming. You can give multiple file extensions using --ignore_ext <file_extension> multiple times.",
)
@click.option(
    "--safe",
    is_flag=True,
    default=False,
    help="Enable safe mode. This will create a copy of the file or folder before renaming.",
)
def rename_files(folder, file, revert, ignore, ignore_ext, safe):
    validate_inputs(folder, file, revert, ignore, ignore_ext, safe)

    if safe:
        file, folder = give_safe_copy(file, folder)

    if revert:
        if folder:
            with open(os.path.join(folder, ".file_renamer.csv"), "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    os.rename(
                        os.path.join(folder, row[1]),
                        os.path.join(folder, row[0]),
                    )
        elif file:
            filename = os.path.basename(file)
            with open(
                os.path.join(os.path.dirname(file), ".file_renamer.csv"), "r"
            ) as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[1] == filename:
                        os.rename(
                            file, os.path.join(os.path.dirname(file), row[0])
                        )
                        break
        else:
            click.echo("Please provide either a folder or a file to revert.")
    elif folder:
        with open(os.path.join(folder, ".file_renamer.csv"), "w") as f:
            writer = csv.writer(f)
            for filename in os.listdir(folder):
                # TODO: don't rename sub-folder
                if is_file_to_be_ignored(filename, ignore, ignore_ext):
                    continue
                new_filename = apply_rename_conventions(filename)
                writer.writerow([filename, new_filename])
                os.rename(
                    os.path.join(folder, filename),
                    os.path.join(folder, new_filename),
                )
    elif file:
        if is_file_to_be_ignored(file, ignore):
            click.echo(
                "Please provide a valid file to rename. This file cannot be renamed because it's a hidden file (dotfile) or is in the ignore list."
            )
            return

        filename = os.path.basename(file)
        new_filename = apply_rename_conventions(filename)
        with open(
            os.path.join(os.path.dirname(file), ".file_renamer.csv"), "w"
        ) as f:
            writer = csv.writer(f)
            writer.writerow([filename, new_filename])
        os.rename(file, os.path.join(os.path.dirname(file), new_filename))
    else:
        click.echo("Please provide either a folder or a file to rename.")


def validate_inputs(folder, file, revert, ignore, ignore_ext, safe):
    if not folder and not file:
        raise ValueError("Please provide either a folder or a file to rename.")
    if folder and file:
        raise ValueError(
            "Cannot use both --folder and --file flags at the same time."
        )
    # TODO: How will revert work with copy? Should we delete the copy?
    if revert and safe:
        raise ValueError(
            "Cannot use both --revert and --safe flags at the same time."
        )
    # TODO: How can we validate ignore and ignore_ext?


def give_safe_copy(file: str, folder: str) -> Tuple[str, str]:
    if file:
        shutil.copy2(file, file + "_copy")
    if folder:
        shutil.copytree(folder, folder + "_copy")
        folder = folder + "_copy"
    return file, folder


def is_file_to_be_ignored(filename: str, ignore: list, ignore_ext: str) -> bool:
    return (
        filename.startswith(".")
        or any(ignored_file == filename for ignored_file in ignore)
        or any(filename.endswith(ext) for ext in ignore_ext)
    )


def apply_rename_conventions(filename: str) -> str:
    """Apply renaming conventions to a filename."""
    filename = filename.replace(" ", "-").lower()

    # remove all special characters
    filename = re.sub(r"[^a-zA-Z0-9_.-]", "", filename)

    # remove multiple consecutive hyphens
    filename = re.sub(r"-+", "-", filename)

    return filename


if __name__ == "__main__":
    rename_files()
