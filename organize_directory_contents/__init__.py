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


def move_file(file: Path, target_dir: Path) -> None:
    """Move `file` into `target_dir`."""

    file.rename(target_dir / file.name)


def move_extensionless(
    file: Path, root_dir: Path, targets: defaultdict[str, str]
) -> None:
    """Move a file without an extension."""

    target_dir = MISC_DIR
    try:
        with file.open("r", encoding="utf-8") as f:
            header = f.readline().lower()

    except (IOError, UnicodeDecodeError):
        pass  # Do nothing because the target defaults to `MISC_DIR`

    else:
        if "python3" in header:
            target_dir = targets["py"]

        elif "sh" in header:
            target_dir = targets["sh"]

    move_file(file, root_dir / target_dir)


def move_image(image_file: Path, target_dir: Path) -> None:
    """Move an image and its sidecar file to `target_dir`."""

    move_file(image_file, target_dir)

    sidecar_file = image_file.with_suffix(".xmp")
    try:
        move_file(sidecar_file, target_dir)
    except FileNotFoundError:
        pass  # Do nothing if a sidecar file does not exist.


__all__ = (
    "MISC_DIR",
    "read_targets_from_file",
    "move_file",
    "move_extensionless",
    "move_image",
)
