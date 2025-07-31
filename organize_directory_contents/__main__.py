"""A CLI script to organize the contents of a directory"""

__author__ = "Charles Mesa Cayobit"


from argparse import ArgumentParser
from pathlib import Path

from organize_directory_contents.main import main

if __name__ == "__main__":
    parser = ArgumentParser(prog="Organize Directory", description=__doc__)
    parser.add_argument("dir", type=Path, help="the directory to organize")
    parser.add_argument(
        "-t",
        "--targets",
        type=Path,
        help="a map between a file extension and its destination",
    )
    args = parser.parse_args()
    targets_file = args.targets or args.dir / "targets.cfg"

    main(args.dir, targets_file)
