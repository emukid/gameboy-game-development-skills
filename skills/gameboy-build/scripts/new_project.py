#!/usr/bin/env python3
"""Copy the bundled GBDK starter into a new directory without overwriting files."""
import argparse
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    destination = args.destination.expanduser().resolve()
    if destination.exists():
        parser.error(f"destination already exists: {destination}")
    source = Path(__file__).resolve().parents[1] / "assets" / "starter"
    shutil.copytree(source, destination)
    print(destination)


if __name__ == "__main__":
    main()
