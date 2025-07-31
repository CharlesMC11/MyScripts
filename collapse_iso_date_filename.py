#!/usr/bin/env python3 -OO
"""Collapse a filename that follows `YYYY-MM-DDThh:mm:ss±z.ext`."""


from argparse import ArgumentParser
from pathlib import Path

YEAR_FMT = "YYYY"
MONTH_FMT = "MM"
DAY_FMT = "DD"

HOUR_FMT = "hh"
MIN_FMT = "mm"
SEC_FMT = "ss"

DATE_FMT = f"{YEAR_FMT}-{MONTH_FMT}-{DAY_FMT}"
TIME_FMT = f"T{HOUR_FMT}:{MIN_FMT}:{SEC_FMT}"
Z_FMT = f"±{HOUR_FMT}"

DATETIME_STR_LENGTH = len(DATE_FMT) + len(TIME_FMT) + len(Z_FMT)


def main(prefix_delim: str = "_", date_sep: str = "-") -> None:
    cwd = Path(".").resolve()
    print(f"Reformating date prefixes in '{cwd.name}':\n")

    for dir in cwd.iterdir():
        filename_start = dir.stem.strip()[:DATETIME_STR_LENGTH]

        try:
            date_prefix = filename_start.split(prefix_delim, 1)[0]
            int(date_prefix)
        except ValueError:
            continue

        prefix_length = len(date_prefix)
        if prefix_length <= 4:
            continue

        year = date_prefix[:4]
        month = date_prefix[4:6]
        day = date_prefix[6:] or None

        formatted = f"{year}{date_sep}{month}"
        if day is not None:
            formatted = f"{formatted}{date_sep}{day}"

        # if date_prefix[-3:] != "+":
        #     formatted = f"{formatted}+08"

        new_filename = dir.name.replace(date_prefix, formatted).strip()

        print(f"'{dir.name}' to:\n'{new_filename}'\n")
        dir.rename(new_filename)


if __name__ == "__main__":
    parser = ArgumentParser(prog="Split Date Prefix", description=__doc__)
    parser.add_argument("dir", type=Path, help="directories")
    args = parser.parse_args()
    main()
