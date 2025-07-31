# Personal Scripts

## `organize_directory_contents`

A script originally intended to organize my Downloads folder. A `targets.cfg`
file contains which subdirectories files with particular extensions should be
sent to. This `targets.cfg` file can be given to the script as an argument or
placed within the same directory that will be organized.

## `process_screenshots`

A script that renames and adds certain metadata to screenshots taken on my
laptop. `main.zsh` can be directly used in the terminal, while `workflow.zsh` is
intended to be sourced by a MacOS Folder Action.

## `collapse_iso_date_filename`

## `isolate_dangling_xmp_files`

A script that will recursively search a directory for XMP files that don't have
corresponding image files, then move them to a new directory.

## `lower_file_extensions`

A script that will recursively search a directory for files with non-lowercase
extensions, then rename them.
