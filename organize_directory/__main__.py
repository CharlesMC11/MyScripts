"""A CLI script to organize the contents of a directory"""

__author__ = "Charles Mesa Cayobit"


from argparse import ArgumentParser
from pathlib import Path

import organize_directory.targets as targets
from organize_directory import *


def main(root_dir: Path) -> None:

    for dir in targets.DIRECTORIES:
        (root_dir / dir).mkdir(parents=True, exist_ok=True)

    # `move_image()` will move an image's existing sidecar file alongside the
    # image, so defer processing XMP files to the end.
    xmp_files: list[Path] = []

    for file in root_dir.iterdir():
        if file.name in targets.DIRECTORIES or file.name == ".DS_Store":
            continue

        elif file.is_dir():
            move_file(file, root_dir / targets.MISC)
            continue

        file_ext = file.suffix
        if not file_ext:
            move_extensionless(file, root_dir)
            continue

        file_ext = file_ext[1:].lower()
        if file_ext == "xmp":
            xmp_files.append(file)
            continue

        target_dir = targets.TARGETS[file_ext]
        if target_dir == targets.IMAGES or target_dir == targets.IMAGES_RAW:
            move_image(file, root_dir / target_dir)

        else:
            move_file(file, root_dir / target_dir)

    for xmp_file in xmp_files:
        try:
            move_file(xmp_file, root_dir / targets.MISC)
        except FileNotFoundError:
            pass  # Do nothing if the image sidecar file had already been moved.


if __name__ == "__main__":
    parser = ArgumentParser(prog="Organize Directory", description=__doc__)
    parser.add_argument("dir", type=Path, help="the directory to organize")
    args = parser.parse_args()

    main(args.dir)
