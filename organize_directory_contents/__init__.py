__author__ = "Charles Mesa Cayobit"


from collections import defaultdict
from pathlib import Path

MISC_DIR = "Misc"


def read_targets_from_file(
    file: Path,
) -> tuple[frozenset[str], defaultdict[str, str]]:
    """Create a targets mapping from a file."""

    dirs: set[str] = set()
    targets: defaultdict[str, str] = defaultdict(lambda: MISC_DIR)

    with file.open() as f:
        for line in f:
            if not line or line.startswith("#"):
                continue
            try:
                key, value = line.split("=")
            except ValueError:
                continue

            value = value.strip()
            dirs.add(value)
            targets[key.strip()] = value

    dirs.add(MISC_DIR)
    return frozenset(dirs), targets


__all__ = "MISC_DIR", "move_file", "move_image", "read_from_file"
