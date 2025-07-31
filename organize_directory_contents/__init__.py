__author__ = "Charles Mesa Cayobit"


from pathlib import Path

MISC_DIR = "Misc"


def move_file(file: Path, target_dir: Path) -> None:
    """Move `file` into `target_dir`."""

    file.rename(target_dir / file.name)


def move_image(image_file: Path, target_dir: Path) -> None:
    """Move an image and its sidecar file to `target_dir`."""

    move_file(image_file, target_dir)

    sidecar_file = image_file.with_suffix(".xmp")
    try:
        move_file(sidecar_file, target_dir)
    except FileNotFoundError:
        pass  # Do nothing if a sidecar file does not exist.


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


__all__ = "MISC_DIR", "move_file", "move_image", "read_from_file"
