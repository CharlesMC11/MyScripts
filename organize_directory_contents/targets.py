__author__ = "Charles Mesa Cayobit"


from pathlib import Path

MISC_DIR = "Misc"


def read_from_file(file: Path) -> tuple[set[str], dict[str, str]]:
    """Create a targets dictionary from a file."""

    dirs: set[str] = set()
    targets: dict[str, str] = {}
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
    return dirs, targets
